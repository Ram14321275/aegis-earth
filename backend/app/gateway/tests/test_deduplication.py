import asyncio
import pytest
from unittest.mock import AsyncMock

from app.gateway.deduplication import RequestCoalescer

# We mock Redis to avoid needing a live Redis instance for tests
class MockPubSub:
    async def subscribe(self, *args):
        pass
    async def unsubscribe(self, *args):
        pass
    async def close(self):
        pass
    async def listen(self):
        # Yield nothing, simulating timeout if wait is long
        await asyncio.sleep(0.5)
        yield {"type": "message", "data": b'{"status": "ok"}'}


class MockRedis:
    def __init__(self):
        self.locks = set()
        
    async def set(self, key, value, nx=False, ex=None):
        if nx and key in self.locks:
            return False
        self.locks.add(key)
        return True
        
    async def publish(self, channel, message):
        pass
        
    async def delete(self, key):
        self.locks.discard(key)
        
    def pubsub(self):
        return MockPubSub()


@pytest.mark.asyncio
async def test_request_coalescing_concurrency(monkeypatch):
    mock_redis = MockRedis()
    
    # Mock redis client
    async def get_mock_client():
        return mock_redis
        
    monkeypatch.setattr("app.gateway.deduplication.redis_client.get_client", get_mock_client)
    
    coalescer = RequestCoalescer()
    
    execution_count = 0
    
    async def expensive_action():
        nonlocal execution_count
        execution_count += 1
        await asyncio.sleep(0.1) # Simulate work
        return {"status": "ok"}
        
    # Fire 10 concurrent requests
    payload = {"query": "flood_hyderabad"}
    tasks = [
        coalescer.execute_coalesced(payload, "1.0", "v1", expensive_action)
        for _ in range(10)
    ]
    
    results = await asyncio.gather(*tasks)
    
    # Only 1 execution should have happened!
    assert execution_count == 1
    
    # All 10 callers should get the same result
    for r in results:
        assert r["status"] == "ok"
