import pytest
from app.core.edge.offline.queue import offline_queue
from app.core.edge.recovery.engine import recovery_engine
from app.core.edge.synchronization.checkpoints import checkpoint_manager

@pytest.mark.asyncio
async def test_offline_recovery():
    # Setup
    offline_queue._queues = {}
    offline_queue.enqueue_event("node_recovery_1", {"event_id": "ev_1", "parent_event_id": "ev_0"})
    offline_queue.enqueue_event("node_recovery_1", {"event_id": "ev_2", "parent_event_id": "ev_1"})
    
    checkpoint_manager.update_checkpoint("node_recovery_1", "ev_0")
    
    # Run recovery
    success = await recovery_engine.initiate_recovery("node_recovery_1")
    
    assert success is True
    # Queue should be empty now
    assert len(offline_queue.get_queued_events("node_recovery_1")) == 0
    # Checkpoint should be updated
    assert checkpoint_manager.get_checkpoint("node_recovery_1") == "ev_2"
    
@pytest.mark.asyncio
async def test_corrupted_offline_recovery():
    # Setup corrupted queue (lineage gap)
    offline_queue._queues = {}
    offline_queue.enqueue_event("node_recovery_2", {"event_id": "ev_1", "parent_event_id": "ev_0"})
    offline_queue.enqueue_event("node_recovery_2", {"event_id": "ev_3", "parent_event_id": "ev_X"})
    
    success = await recovery_engine.initiate_recovery("node_recovery_2")
    
    # Should fail due to lineage verification failure
    assert success is False
