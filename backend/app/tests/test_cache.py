import asyncio
from unittest.mock import AsyncMock, patch

from app.core.cache.distributed_lock import DistributedLock
from app.core.cache.manager import cache_manager
from app.core.cache.redis_client import redis_client


def test_redis_connectivity():
    async def run_test():
        mock_client = AsyncMock()
        mock_client.ping.return_value = True

        with patch("app.core.cache.redis_client.redis_client.get_client", return_value=mock_client):
            client = await redis_client.get_client()
            assert client is not None
            assert await client.ping()

    asyncio.run(run_test())


def test_cache_hit_miss():
    async def run_test():
        mock_client = AsyncMock()
        # Initial get (fast path) -> miss
        # Second get (slow path recheck) -> miss
        # Third get (second call fast path) -> hit
        mock_client.get.side_effect = [None, None, '{"data": "value"}']
        
        # Test fetch function
        async def fetch():
            return {"data": "value"}

        with patch("app.core.cache.redis_client.redis_client.get_client", return_value=mock_client):
            # We mock the lock to do nothing since this tests hit/miss
            with patch("app.core.cache.distributed_lock.DistributedLock.__aenter__") as mock_lock:
                mock_lock.return_value = None
                
                # Miss path
                val, hit = await cache_manager.get_or_fetch("test_key", fetch, ttl_seconds=60)
                assert val == {"data": "value"}
                assert not hit
                mock_client.set.assert_called_once()
                
                # Hit path
                val, hit = await cache_manager.get_or_fetch("test_key", fetch, ttl_seconds=60)
                assert val == {"data": "value"}
                assert hit
                
    asyncio.run(run_test())


def test_distributed_lock_acquisition():
    async def run_test():
        mock_client = AsyncMock()
        mock_client.set.return_value = True  # Successfully acquired

        with patch("app.core.cache.redis_client.redis_client.get_client", return_value=mock_client):
            lock = DistributedLock("test_lock", timeout_ms=5000)
            async with lock:
                assert lock._acquired
                mock_client.set.assert_called_with("lock:test_lock", lock.token, nx=True, px=5000)
                
            # Exit should call eval to release
            mock_client.eval.assert_called_once()
            
    asyncio.run(run_test())


def test_distributed_lock_timeout_handling():
    async def run_test():
        mock_client = AsyncMock()
        # Simulate lock already held, so set returns False
        # To avoid infinite loop, we limit the number of returns or raise an exception
        # Let's test that if set returns False, it waits and retries.
        # We will make it return False once, then True
        mock_client.set.side_effect = [False, True]

        with patch("app.core.cache.redis_client.redis_client.get_client", return_value=mock_client):
            with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
                lock = DistributedLock("test_lock", timeout_ms=5000, retry_delay_ms=10)
                async with lock:
                    assert lock._acquired
                
                assert mock_sleep.call_count == 1
                mock_client.eval.assert_called_once()
                
    asyncio.run(run_test())


def test_cache_stampede_prevention():
    async def run_test():
        fetch_call_count = 0
        
        async def slow_fetch():
            nonlocal fetch_call_count
            fetch_call_count += 1
            await asyncio.sleep(0.1)
            return {"data": "slow"}

        mock_client = AsyncMock()
        # Both coroutines get None from cache initially
        # The first acquires the lock, fetches, and saves.
        # The second waits for the lock. After acquiring, it should find the data in cache.
        
        state = {"locked": False, "cache": None}
        
        async def mock_get(key):
            return state["cache"]
            
        async def mock_set_cache(key, value, ex):
            state["cache"] = value
            return True
            
        async def mock_set_lock(key, value, nx, px):
            if state["locked"]:
                return False
            state["locked"] = True
            return True
            
        async def mock_eval(*args):
            state["locked"] = False
            return 1
            
        mock_client.get.side_effect = mock_get
        mock_client.set.side_effect = mock_set_cache # for cache service
        
        # We will need to differentiate between cache SET and lock SET
        # But wait, cache_service uses client.set(key, val, ex=ttl), distributed_lock uses nx=True, px=ttl
        async def side_effect_set(*args, **kwargs):
            if "nx" in kwargs:
                return await mock_set_lock(*args, **kwargs)
            else:
                return await mock_set_cache(*args, **kwargs)
                
        mock_client.set.side_effect = side_effect_set
        mock_client.eval.side_effect = mock_eval
        
        with patch("app.core.cache.redis_client.redis_client.get_client", return_value=mock_client):
            # Run two concurrent get_or_fetch calls
            results = await asyncio.gather(
                cache_manager.get_or_fetch("stampede_key", slow_fetch),
                cache_manager.get_or_fetch("stampede_key", slow_fetch)
            )
            
            assert results[0][0] == {"data": "slow"}
            assert results[1][0] == {"data": "slow"}
            
            # The fetch function should only be called once despite 2 concurrent requests
            assert fetch_call_count == 1

    asyncio.run(run_test())


def test_cache_key_builder():
    from app.core.cache.cache_keys import CacheCategory, CacheKeyBuilder
    
    loc_key = CacheKeyBuilder.location_search("Hyderabad ")
    assert loc_key == "v1:location_search:hyderabad"

    coord_key = CacheKeyBuilder.coordinates(CacheCategory.ALERTS, 17.38504, 78.48667)
    assert coord_key == "v1:alerts:tile:z12:x2941:y1847"
