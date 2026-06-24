import pytest
from app.core.edge.synchronization.orchestrator import sync_orchestrator
from app.core.edge.synchronization.checkpoints import checkpoint_manager

@pytest.mark.asyncio
async def test_synchronization_orchestrator():
    # Setup initial checkpoint
    checkpoint_manager.update_checkpoint("node_1", "event_A")
    
    # Valid batch (lineage maintained)
    events_valid = [{"event_id": "event_B", "parent_event_id": "event_A"}, {"event_id": "event_C", "parent_event_id": "event_B"}]
    success = await sync_orchestrator.process_sync_batch("node_1", events_valid)
    assert success is True
    assert checkpoint_manager.get_checkpoint("node_1") == "event_C"
    
    # Invalid batch (lineage gap)
    events_invalid = [{"event_id": "event_E", "parent_event_id": "event_D"}]
    success = await sync_orchestrator.process_sync_batch("node_1", events_invalid)
    assert success is False
    assert checkpoint_manager.get_checkpoint("node_1") == "event_C"
