import pytest
from app.core.edge.reconciliation.engine import conflict_engine

def test_reconciliation_engine():
    base_state = {"payload_hash": "hash_base"}
    branch_a = {"payload_hash": "hash_a", "timestamp": "2026-06-24T10:00:00Z"}
    branch_b = {"payload_hash": "hash_b", "timestamp": "2026-06-24T09:00:00Z"}
    
    # Branch B is older, should win via timestamp arbitration
    winning_state, event = conflict_engine.resolve_divergence(base_state, branch_a, branch_b)
    
    assert winning_state["payload_hash"] == "hash_b"
    assert event["resolved_hash"] == "hash_b"
    assert event["base_hash"] == "hash_base"
    assert event["type"] == "RECONCILIATION"
