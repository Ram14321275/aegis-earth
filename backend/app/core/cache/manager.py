import asyncio
from typing import Any, Callable, Optional

from app.core.cache.distributed_lock import DistributedLock
from app.core.cache.service import CacheService
from app.observability.metrics import metrics_store


class CacheManager:
    def __init__(self):
        self.service = CacheService()

    async def get_or_fetch(
        self,
        key: str,
        fetch_func: Callable[..., Any],
        ttl_seconds: Optional[int] = None,
    ) -> tuple[Any, bool]:
        # Fast path
        val = await self.service.get(key)
        if val is not None:
            metrics_store.record_cache_access(hit=True)
            return val, True

        # Deduplication slow path
        async with DistributedLock(key, timeout_ms=10000):
            # Recheck after acquiring lock
            val = await self.service.get(key)
            if val is not None:
                metrics_store.record_cache_access(hit=True)
                return val, True

            # Fetch
            metrics_store.record_cache_access(hit=False)
            val = await fetch_func()

            if val is not None:
                kwargs = {}
                if ttl_seconds is not None:
                    kwargs["ttl_seconds"] = ttl_seconds
                await self.service.set(key, val, **kwargs)

            return val, False

    async def invalidate(self, key: str):
        await self.service.invalidate(key)

    async def get_status(self) -> dict:
        return {
            "status": "healthy",
            "availability": "100%",
            "metrics_summary": {"entry_count": await self.service.get_entry_count()},
        }


cache_manager = CacheManager()
