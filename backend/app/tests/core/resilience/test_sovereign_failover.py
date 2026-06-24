import pytest
from app.core.resilience.failover.promotion import failover_promoter

def test_sovereign_failover():
    res = failover_promoter.promote_node("node-1", "node-2", "US-EAST", "US-WEST")
    assert res["status"] == "PROMOTED"
    assert "fencing_token" in res

def test_sovereignty_violation():
    res = failover_promoter.promote_node("node-1", "node-2", "US-EAST", "EU-WEST")
    assert res["status"] == "FAILED"
    assert res["reason"] == "SOVEREIGNTY_VIOLATION"
