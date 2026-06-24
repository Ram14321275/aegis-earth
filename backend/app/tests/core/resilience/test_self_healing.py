import pytest
from app.core.resilience.healing.engine import healing_engine

def test_safe_healing():
    res = healing_engine.trigger_healing("clear_cache", "node_1")
    assert res["status"] == "EXECUTED"
    assert res["category"] == "SAFE_AUTOMATION"
    assert res["reasoning_hash"] is not None

def test_approval_healing():
    res = healing_engine.trigger_healing("restart_worker_pool", "node_1")
    assert res["status"] == "PENDING_APPROVAL"
    assert res["category"] == "APPROVAL_REQUIRED"

def test_forbidden_healing():
    res = healing_engine.trigger_healing("drop_database", "node_1")
    assert res["status"] == "FAILED"
    assert res["reason"] == "FORBIDDEN"
