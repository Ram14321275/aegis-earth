import pytest
from app.core.governance.audit.audit_engine import ImmutableAuditEngine
from app.core.governance.audit.signatures import HMACSHA256Provider
from app.core.governance.audit.chain import AuditChainValidator

@pytest.mark.asyncio
async def test_immutable_audit_chain():
    provider = HMACSHA256Provider("test-secret-key", "v1")
    engine = ImmutableAuditEngine(provider)
    
    event1 = await engine.record_event("tenant_1", "actor_1", "TEST_ACTION", {"k": "v1"})
    event2 = await engine.record_event("tenant_1", "actor_1", "TEST_ACTION_2", {"k": "v2"}, parent_lineage=event1["lineage_path"])
    event3 = await engine.record_event("tenant_1", "actor_2", "TEST_ACTION_3", {"k": "v3"}, parent_lineage=event2["lineage_path"])
    
    events = [event1, event2, event3]
    
    # Verify chain
    assert AuditChainValidator.verify_chain(events) is True
    
    # Tamper with payload hash of event2
    events[1]["payload_hash"] = "tampered_hash"
    assert AuditChainValidator.verify_chain(events) is False
