import pytest
from app.core.streaming.websocket import WebSocketManager, MAX_OUTBOUND_QUEUE_SIZE
from app.core.streaming.models import FloodEvent

class MockWebSocket:
    def __init__(self):
        self.closed = False
        self.code = None
        
    async def accept(self):
        pass
        
    async def send_text(self, data: str):
        if self.closed:
            raise Exception("Cannot send on closed websocket")
            
    async def close(self, code=1000):
        self.closed = True
        self.code = code

@pytest.mark.anyio
async def test_websocket_manager_connect_disconnect():
    manager = WebSocketManager()
    ws = MockWebSocket()
    
    conn_id = await manager.connect(ws) # type: ignore
    assert conn_id in manager.active_connections
    
    await manager.disconnect(conn_id)
    assert conn_id not in manager.active_connections
    assert ws.closed
    assert ws.code == 1000

@pytest.mark.anyio
async def test_websocket_manager_backpressure():
    manager = WebSocketManager()
    ws = MockWebSocket()
    
    conn_id = await manager.connect(ws) # type: ignore
    
    # Simulate slow client by filling the queue manually
    ctx = manager.active_connections[conn_id]
    
    for i in range(MAX_OUTBOUND_QUEUE_SIZE):
        success = ctx.enqueue(f"msg_{i}")
        assert success == True
        
    # The next enqueue should fail
    success = ctx.enqueue("overflow")
    assert success == False
    
    # Since safe_enqueue handles overflow by disconnecting
    manager._safe_enqueue(conn_id, "overflow")
    
    # Needs a small sleep to allow the background disconnect task to run
    import asyncio
    await asyncio.sleep(0.1)
    
    assert conn_id not in manager.active_connections
