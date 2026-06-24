import pytest
from app.core.cyber.forensics.engine import forensic_engine

def test_forensic_reconstruction():
    events_valid = [
        {"id": "e1", "hash": "h1"},
        {"id": "e2", "hash": "h2", "parent_hash": "h1"}
    ]
    res = forensic_engine.reconstruct_attack_timeline("inc_1", events_valid)
    assert res["lineage_valid"] is True
    
    events_invalid = [
        {"id": "e1", "hash": "h1"},
        {"id": "e2", "hash": "h2", "parent_hash": "hX"} # Broken link
    ]
    res = forensic_engine.reconstruct_attack_timeline("inc_2", events_invalid)
    assert res["lineage_valid"] is False
