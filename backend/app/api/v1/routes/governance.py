from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
from datetime import datetime

from app.core.governance.audit.audit_engine import audit_engine
from app.core.governance.approvals.workflow import approval_engine
from app.core.governance.replay.engine import replay_engine
from app.core.governance.policies.engine import governance_policy_engine
from app.core.governance.compliance.export import compliance_exporter

router = APIRouter(prefix="/governance", tags=["governance"])

@router.get("/audit")
async def search_audit_events():
    """Search audit events."""
    # MVP: Mock response
    return {"events": []}

@router.post("/replay")
async def start_replay_session(tenant_id: str, timestamp: datetime):
    """Start a forensic replay session."""
    return await replay_engine.reconstruct_state(timestamp, tenant_id)

@router.post("/approvals/request")
async def request_approval(tenant_id: str, requester_id: str, action: str, payload: Dict[str, Any]):
    """Initiate a critical action approval request."""
    return {"request_id": await approval_engine.request_approval(tenant_id, requester_id, action, payload, ["admin"])}

@router.post("/approvals/{request_id}/decide")
async def decide_approval(tenant_id: str, approver_id: str, request_id: str, decision: str, reasoning: str):
    """Record an approval decision."""
    try:
        success = await approval_engine.decide_approval(tenant_id, approver_id, request_id, decision, reasoning)
        return {"success": success, "decision": decision}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/compliance/export")
async def export_compliance_evidence(tenant_id: str, requester_id: str, format_type: str):
    """Generate compliance export."""
    try:
        return await compliance_exporter.generate_export(tenant_id, requester_id, [], format_type)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/policies/evaluate")
async def evaluate_policy(policy_name: str, context: Dict[str, Any]):
    """Evaluate a governance policy."""
    allowed = governance_policy_engine.evaluate_policy(policy_name, context)
    return {"policy": policy_name, "allowed": allowed}
