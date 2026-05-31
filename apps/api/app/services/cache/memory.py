from datetime import datetime, timedelta, timezone
from threading import Lock
from typing import Generic, TypeVar

T = TypeVar("T")


class InMemoryTTLCache(Generic[T]):
    def __init__(self, ttl_seconds: int = 900) -> None:
        self.ttl = timedelta(seconds=ttl_seconds)
        self._items: dict[str, tuple[datetime, T]] = {}
        self._lock = Lock()

    def get(self, key: str) -> T | None:
        with self._lock:
            item = self._items.get(key)
            if item is None:
                return None

            expires_at, value = item
            if expires_at <= datetime.now(timezone.utc):
                self._items.pop(key, None)
                return None

            return value

    def set(self, key: str, value: T) -> None:
        with self._lock:
            self._items[key] = (datetime.now(timezone.utc) + self.ttl, value)


request_cache: InMemoryTTLCache = InMemoryTTLCache()

