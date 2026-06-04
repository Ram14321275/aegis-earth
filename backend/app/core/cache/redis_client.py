import logging
from typing import Optional

from redis.asyncio import ConnectionPool, Redis
from redis.exceptions import ConnectionError, RedisError

from app.core.config import get_settings

logger = logging.getLogger(__name__)


class RedisClient:
    _instance = None
    _client: Optional[Redis] = None
    _pool: Optional[ConnectionPool] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisClient, cls).__new__(cls)
        return cls._instance

    async def connect(self):
        if self._client is None:
            settings = get_settings()
            try:
                self._pool = ConnectionPool.from_url(
                    settings.redis_url,
                    decode_responses=True,
                    max_connections=10,
                    socket_connect_timeout=1.0,
                    socket_timeout=1.0,
                )
                self._client = Redis(connection_pool=self._pool)
                # Verify connection
                await self._client.ping()
                logger.info("Successfully connected to Redis.")
            except RedisError as e:
                logger.error(f"Failed to connect to Redis: {e}")
                self._client = None
                self._pool = None

    async def close(self):
        if self._client:
            await self._client.aclose()
            self._client = None
            self._pool = None

    @property
    def client(self) -> Optional[Redis]:
        return self._client

    async def get_client(self) -> Optional[Redis]:
        if self._client is None:
            await self.connect()
        return self._client

    async def ping(self) -> bool:
        client = await self.get_client()
        if not client:
            return False
        try:
            return await client.ping()
        except RedisError:
            # Clear client so it reconnects next time
            self._client = None
            return False


redis_client = RedisClient()
