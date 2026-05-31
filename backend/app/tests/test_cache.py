import pytest

from app.services.cache.service import CacheKeyBuilder, CacheService, get_cache_service


def test_cache_key_builder():
    assert CacheKeyBuilder.location("Hyderabad") == "v1:location:hyderabad"
    assert CacheKeyBuilder.location("  HYDERABAD  ") == "v1:location:hyderabad"
    assert (
        CacheKeyBuilder.coordinates(17.38501, 78.48679)
        == "v1:coordinates:17.3850:78.4868"
    )
    assert CacheKeyBuilder.coordinates(17.3, 78.4) == "v1:coordinates:17.3000:78.4000"


def test_cache_service_set_get():
    cache = CacheService()
    cache.set("key1", "value1")
    assert cache.get("key1") == "value1"
    stats = cache.get_stats()
    assert stats["hits"] == 1
    assert stats["misses"] == 0
    assert stats["entry_count"] == 1


def test_cache_service_ttl():
    cache = CacheService()
    # Expire immediately
    cache.set("key_expire", "val", ttl_hours=-1)

    val = cache.get("key_expire")
    assert val is None
    stats = cache.get_stats()
    assert stats["misses"] == 1
    # Invalidated upon get
    assert stats["entry_count"] == 0


def test_cache_service_invalidate_clear():
    cache = CacheService()
    cache.set("key1", "value1")
    cache.invalidate("key1")
    assert cache.get("key1") is None

    cache.set("key2", "value2")
    cache.clear()
    assert cache.get("key2") is None
    assert cache.get_stats()["entry_count"] == 0


def test_cache_singleton():
    cache1 = get_cache_service()
    cache2 = get_cache_service()
    assert cache1 is cache2
