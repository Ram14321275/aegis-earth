import json
import logging
from typing import Any, Optional

from app.core.cache.cache_policies import CachePolicy
from app.core.cache.redis_client import redis_client

logger = logging.getLogger(__name__)


class CacheService:
    def __init__(self):
        pass

    async def get(self, key: str) -> Optional[Any]:
        client = await redis_client.get_client()
        if not client:
            logger.warning("Redis client unavailable, bypassing cache GET.")
            return None

        try:
            val = await client.get(key)
            if val is not None:
                return json.loads(val)
            return None
        except Exception as e:
            logger.error(f"Error reading from Redis cache: {e}")
            return None

    async def set(
        self,
        key: str,
        value: Any,
        ttl_seconds: int = CachePolicy.DEFAULT_TTL_SECONDS,
    ) -> None:
        client = await redis_client.get_client()
        if not client:
            logger.warning("Redis client unavailable, bypassing cache SET.")
            return

        try:
            val_json = json.dumps(value)
            await client.set(key, val_json, ex=ttl_seconds)
        except Exception as e:
            logger.error(f"Error writing to Redis cache: {e}")

    async def invalidate(self, key: str) -> None:
        client = await redis_client.get_client()
        if not client:
            return
        
        try:
            await client.delete(key)
        except Exception as e:
            logger.error(f"Error invalidating Redis cache key: {e}")

    async def clear(self) -> None:
        client = await redis_client.get_client()
        if not client:
            return
        
        try:
            await client.flushdb()
        except Exception as e:
            logger.error(f"Error clearing Redis cache: {e}")

    async def get_entry_count(self) -> int:
        client = await redis_client.get_client()
        if not client:
            return 0
        
        try:
            return await client.dbsize()
        except Exception as e:
            logger.error(f"Error getting Redis DB size: {e}")
            return 0
