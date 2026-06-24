import pytest
from app.core.governance.approvals.workflow import ApprovalWorkflowEngine

@pytest.mark.asyncio
async def test_approvals_workflow():
    engine = ApprovalWorkflowEngine()
    
    # Request
    request_id = await engine.request_approval("tenant_1", "actor_1", "MASS_ALERT", {}, ["admin"])
    assert request_id is not None
    
    # Decide
    success = await engine.decide_approval("tenant_1", "admin_1", request_id, "APPROVED", "Situation confirmed")
    assert success is True
    
    # Invalid decision
    with pytest.raises(ValueError):
        await engine.decide_approval("tenant_1", "admin_1", request_id, "MAYBE", "Unsure")
