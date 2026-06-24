import pytest
from app.core.cyber.containment.engine import containment_engine

def test_containment_execution():
    res = containment_engine.trigger_containment("websocket_quarantine", "tenant_a", "hash_123", enterprise_tenant=False)
    assert res["status"] == "EXECUTED"
    assert res["type"] == "websocket_quarantine"
    assert "rollback_strategy" in res
    
def test_containment_approval_gating():
    res = containment_engine.trigger_containment("temporary_tenant_isolation", "tenant_ent", "hash_abc", enterprise_tenant=True)
    assert res["status"] == "PENDING_APPROVAL"
    assert res["approval_required"] is True
