import asyncio
import logging
import time
import uuid

from redis.exceptions import RedisError

from app.core.cache.redis_client import redis_client
from app.observability.metrics import metrics_store

logger = logging.getLogger(__name__)


class DistributedLock:
    def __init__(self, name: str, timeout_ms: int = 10000, retry_delay_ms: int = 50):
        self.name = f"lock:{name}"
        self.timeout_ms = timeout_ms
        self.retry_delay_ms = retry_delay_ms
        self.token = str(uuid.uuid4())
        self._acquired = False

    async def __aenter__(self):
        start_time = time.time()
        client = await redis_client.get_client()

        if not client:
            # Fallback behavior if Redis is down
            logger.warning("Redis client unavailable, bypassing distributed lock.")
            self._acquired = False
            return self

        while True:
            try:
                # Attempt to acquire the lock (NX = Set if Not eXists, PX = Expiration time in ms)
                acquired = await client.set(
                    self.name, self.token, nx=True, px=self.timeout_ms
                )
                if acquired:
                    self._acquired = True
                    metrics_store.record_redis_lock(acquired=True, wait_ms=(time.time() - start_time) * 1000)
                    return self
            except RedisError as e:
                logger.error(f"Redis error while acquiring lock: {e}")
                metrics_store.record_redis_error()
                self._acquired = False
                return self

            # Wait before retrying
            await asyncio.sleep(self.retry_delay_ms / 1000.0)
            
            # Check if we've waited too long (optional safety mechanism to prevent infinite loop)
            # if (time.time() - start_time) * 1000 > self.timeout_ms * 2:
            #     raise TimeoutError("Failed to acquire distributed lock")

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not self._acquired:
            return

        client = await redis_client.get_client()
        if not client:
            return

        try:
            # Only release if the token matches (Lua script for atomicity)
            script = """
            if redis.call("get", KEYS[1]) == ARGV[1] then
                return redis.call("del", KEYS[1])
            else
                return 0
            end
            """
            await client.eval(script, 1, self.name, self.token)
        except RedisError as e:
            logger.error(f"Redis error while releasing lock: {e}")
            metrics_store.record_redis_error()
