from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from pydantic import BaseModel

from app.core.logging import get_logger

logger = get_logger(__name__)


class CacheEntry(BaseModel):
    key: str
    value: Any
    created_at: datetime
    expires_at: datetime
    source: str
    version: str


class CacheKeyBuilder:
    VERSION = "v1"

    @classmethod
    def location(cls, city: str) -> str:
        return f"{cls.VERSION}:location:{city.lower().strip()}"

    @classmethod
    def coordinates(cls, lat: float, lon: float) -> str:
        # Round to 4 decimal places
        lat_rounded = f"{lat:.4f}"
        lon_rounded = f"{lon:.4f}"
        return f"{cls.VERSION}:coordinates:{lat_rounded}:{lon_rounded}"


class CacheService:
    def __init__(self):
        self._cache: dict[str, CacheEntry] = {}
        self._hits = 0
        self._misses = 0

    def _now(self) -> datetime:
        return datetime.now(timezone.utc)

    def get(self, key: str) -> Optional[Any]:
        entry = self._cache.get(key)
        if not entry:
            self._misses += 1
            return None

        if self._now() > entry.expires_at:
            # Expired
            self.invalidate(key)
            self._misses += 1
            return None

        self._hits += 1
        return entry.value

    def set(
        self,
        key: str,
        value: Any,
        ttl_hours: int = 24,
        source: str = "in-memory",
        version: str = "v1",
    ) -> None:
        now = self._now()
        expires_at = now + timedelta(hours=ttl_hours)
        entry = CacheEntry(
            key=key,
            value=value,
            created_at=now,
            expires_at=expires_at,
            source=source,
            version=version,
        )
        self._cache[key] = entry

    def invalidate(self, key: str) -> None:
        self._cache.pop(key, None)

    def clear(self) -> None:
        self._cache.clear()
        self._hits = 0
        self._misses = 0

    def cleanup_expired(self) -> None:
        now = self._now()
        expired_keys = [k for k, v in self._cache.items() if now > v.expires_at]
        for k in expired_keys:
            self.invalidate(k)

    def get_stats(self) -> dict[str, int]:
        return {
            "hits": self._hits,
            "misses": self._misses,
            "entry_count": len(self._cache),
        }


# Singleton factory
_cache_service_instance = CacheService()


def get_cache_service() -> CacheService:
    return _cache_service_instance
