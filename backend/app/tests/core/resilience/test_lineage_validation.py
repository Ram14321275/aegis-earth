import pytest
from app.core.resilience.lineage.tracker import lineage_tracker

def test_lineage_validation():
    # Construct a valid deterministic chain
    cp1 = {
        "checkpoint_id": "1",
        "snapshot_hash": "snapA",
        "orchestration_hash": "orchA",
        "tenant_id": "t1",
        "region": "US-1"
    }
    hash_1 = lineage_tracker.calculate_checkpoint_hash("snapA", "orchA", "t1", "US-1")
    
    cp2 = {
        "checkpoint_id": "2",
        "snapshot_hash": "snapB",
        "orchestration_hash": "orchB",
        "tenant_id": "t1",
        "region": "US-1",
        "parent_checkpoint_hash": hash_1
    }
    
    assert lineage_tracker.validate_lineage([cp1, cp2]) is True

def test_lineage_corruption():
    cp1 = {"checkpoint_id": "1", "snapshot_hash": "snapA", "orchestration_hash": "orchA", "tenant_id": "t1", "region": "US-1"}
    cp2 = {"checkpoint_id": "2", "parent_checkpoint_hash": "invalid_hash"}
    
    assert lineage_tracker.validate_lineage([cp1, cp2]) is False
