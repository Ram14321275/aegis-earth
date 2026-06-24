import pytest
from app.core.resilience.verification.engine import verification_engine
from app.core.resilience.lineage.tracker import lineage_tracker

def test_verification_sovereignty_abort():
    # Valid lineage but mismatched sovereignty context
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
    
    # Expected region EU-1 mismatches checkpoint region US-1
    assert verification_engine.verify_restoration_chain([cp1, cp2], "EU-1") is False

def test_verification_success():
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
    assert verification_engine.verify_restoration_chain([cp1, cp2], "US-1") is True
