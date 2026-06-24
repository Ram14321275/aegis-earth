import pytest
from app.core.edge.synchronization.checkpoints import checkpoint_manager

def test_checkpoint_restoration():
    checkpoint_manager.update_checkpoint("node_cp_1", "event_99")
    
    cp = checkpoint_manager.get_checkpoint("node_cp_1")
    assert cp == "event_99"
    
    cp_missing = checkpoint_manager.get_checkpoint("node_missing")
    assert cp_missing is None
