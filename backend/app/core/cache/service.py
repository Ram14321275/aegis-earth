import time
from typing import Any, Dict, Optional

from pydantic import BaseModel

from app.core.cache.policies import CachePolicy


class CacheEntry(BaseModel):
    key: str
    value: Any
    created_at: float
    expires_at: float


class CacheService:
    def __init__(self):
        self._store: Dict[str, CacheEntry] = {}

    async def get(self, key: str) -> Optional[Any]:
        entry = self._store.get(key)
        if not entry:
            return None

        if time.time() > entry.expires_at:
            await self.invalidate(key)
            return None

        return entry.value

    async def set(
        self,
        key: str,
        value: Any,
        ttl_seconds: int = CachePolicy.DEFAULT_TTL_SECONDS,
    ) -> None:
        now = time.time()
        self._store[key] = CacheEntry(
            key=key, value=value, created_at=now, expires_at=now + ttl_seconds
        )

    async def invalidate(self, key: str) -> None:
        self._store.pop(key, None)

    async def clear(self) -> None:
        self._store.clear()

    async def get_entry_count(self) -> int:
        return len(self._store)
