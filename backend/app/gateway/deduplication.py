import asyncio
import hashlib
import json
import logging
from typing import Any, Callable, Coroutine, Dict

from app.core.cache.redis_client import redis_client
from app.core.security.tenants import get_current_tenant_id
from app.observability.metrics import metrics_store

logger = logging.getLogger(__name__)


class RequestCoalescer:
    """
    Intelligent in-flight request deduplication via Redis.
    Prevents Thundering Herd scenarios at the API Gateway.
    """

    def __init__(self, lock_timeout_seconds: int = 30):
        self.lock_timeout_seconds = lock_timeout_seconds

    def _generate_fingerprint(
        self, payload: Dict[str, Any], analysis_version: str, provider_version: str
    ) -> str:
        tenant_id = get_current_tenant_id() or "anonymous"
        # Normalize the payload by sorting keys
        normalized_payload = json.dumps(payload, sort_keys=True)
        raw_string = f"{tenant_id}:{normalized_payload}:{analysis_version}:{provider_version}"
        return hashlib.sha256(raw_string.encode("utf-8")).hexdigest()

    async def execute_coalesced(
        self,
        payload: Dict[str, Any],
        analysis_version: str,
        provider_version: str,
        action: Callable[[], Coroutine[Any, Any, Any]],
    ) -> Any:
        fingerprint = self._generate_fingerprint(
            payload, analysis_version, provider_version
        )
        lock_key = f"coalesce:lock:{fingerprint}"
        channel_key = f"coalesce:pubsub:{fingerprint}"

        client = await redis_client.get_client()
        if not client:
            logger.warning("Redis unavailable, bypassing Request Coalescer.")
            return await action()

        # Attempt to become the primary executor
        acquired = await client.set(
            lock_key, "locked", nx=True, ex=self.lock_timeout_seconds
        )

        if acquired:
            logger.debug(f"Acquired coalesce lock for {fingerprint}. Executing...")
            try:
                result = await action()
                # Publish result to waiting consumers
                # Result must be JSON serializable (we assume it's a Pydantic model dump or dict)
                await client.publish(channel_key, json.dumps(result))
                return result
            except Exception as e:
                # Publish error marker
                await client.publish(channel_key, json.dumps({"__coalesce_error": str(e)}))
                raise
            finally:
                await client.delete(lock_key)
        else:
            logger.debug(f"Request coalesced for {fingerprint}. Waiting for primary...")
            metrics_store.record_coalesced_request()
            
            # Subscribe to the channel
            pubsub = client.pubsub()
            await pubsub.subscribe(channel_key)
            try:
                # Wait for the message with a timeout slightly larger than the lock timeout
                async for message in pubsub.listen():
                    if message["type"] == "message":
                        data = json.loads(message["data"].decode("utf-8"))
                        if isinstance(data, dict) and "__coalesce_error" in data:
                            raise Exception(f"Coalesced execution failed: {data['__coalesce_error']}")
                        return data
            except asyncio.TimeoutError:
                logger.warning(f"Coalesce wait timed out for {fingerprint}. Stale lock recovered. Executing independently.")
                # Stale recovery: If the original executor died without publishing, we run it ourselves
                return await action()
            finally:
                await pubsub.unsubscribe(channel_key)
                await pubsub.close()

coalescer = RequestCoalescer()
