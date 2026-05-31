import asyncio
import time

import pytest
from httpx import AsyncClient

from app.core.cache.keys import CacheCategory, CacheKeyBuilder
from app.core.cache.manager import CacheManager
from app.core.cache.service import CacheService
from app.main import app


@pytest.fixture
def cache_service():
    return CacheService()


@pytest.fixture
def cache_manager():
    return CacheManager()


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_cache_hit_miss(cache_service: CacheService):
    key = "test:key"
    assert await cache_service.get(key) is None

    await cache_service.set(key, "data")
    assert await cache_service.get(key) == "data"


@pytest.mark.anyio
async def test_cache_expiration(cache_service: CacheService):
    key = "test:exp"
    await cache_service.set(key, "data", ttl_seconds=1)
    assert await cache_service.get(key) == "data"

    time.sleep(1.1)
    assert await cache_service.get(key) is None


@pytest.mark.anyio
async def test_cache_invalidation(cache_service: CacheService):
    key = "test:inv"
    await cache_service.set(key, "data")
    await cache_service.invalidate(key)
    assert await cache_service.get(key) is None


@pytest.mark.anyio
async def test_cache_deduplication(cache_manager: CacheManager):
    fetch_count = 0

    async def slow_fetch():
        nonlocal fetch_count
        fetch_count += 1
        await asyncio.sleep(0.1)
        return "data"

    key = "test:dedup"

    # Fire 3 concurrent fetches
    results = await asyncio.gather(
        cache_manager.get_or_fetch(key, slow_fetch),
        cache_manager.get_or_fetch(key, slow_fetch),
        cache_manager.get_or_fetch(key, slow_fetch),
    )

    # First fetch executes slow_fetch and returns (data, False)
    # The others wait on the lock and return (data, True)
    hits = sum(1 for val, hit in results if hit)
    misses = sum(1 for val, hit in results if not hit)

    assert fetch_count == 1
    assert hits == 2
    assert misses == 1


def test_cache_key_builder():
    loc_key = CacheKeyBuilder.location_search("Hyderabad ")
    assert loc_key == "v1:location_search:hyderabad"

    coord_key = CacheKeyBuilder.coordinates(CacheCategory.ALERTS, 17.38504, 78.48667)
    assert coord_key == "v1:alerts:17.3850:78.4867"
