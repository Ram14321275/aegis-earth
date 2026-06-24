import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import logging

from app.observability.metrics import metrics_store
from app.core.governance.audit.audit_engine import audit_engine

logger = logging.getLogger(__name__)

class ApprovalWorkflowEngine:
    async def request_approval(
        self, 
        tenant_id: str, 
        requester_id: str, 
        action_type: str, 
        payload: Dict[str, Any],
        required_roles: List[str]
    ) -> str:
        """
        Initiates a critical action approval request.
        """
        metrics_store.record_governance_action("approval_requests_total")
        request_id = f"appreq-{uuid.uuid4()}"
        
        # In a real implementation, store to DB
        # ApprovalRequest(id=request_id, tenant_id=tenant_id, requester_id=requester_id, status='PENDING')
        
        # Audit the request creation natively preserving lineage
        await audit_engine.record_event(
            tenant_id=tenant_id,
            actor_id=requester_id,
            action_type="APPROVAL_REQUESTED",
            payload={"target_action": action_type, "required_roles": required_roles, "original_payload": payload},
            correlation_id=request_id
        )
        
        logger.info(f"Approval request {request_id} created for action {action_type} by {requester_id}")
        return request_id

    async def decide_approval(
        self,
        tenant_id: str,
        approver_id: str,
        request_id: str,
        decision: str, # "APPROVED", "REJECTED"
        reasoning: str
    ) -> bool:
        """
        Records an approval decision cryptographically.
        """
        if decision not in ["APPROVED", "REJECTED"]:
            raise ValueError("Invalid decision")

        # In a real implementation, load request, check if approver has roles, update DB
        # ApprovalDecision(request_id=request_id, approver_id=approver_id, decision=decision)

        await audit_engine.record_event(
            tenant_id=tenant_id,
            actor_id=approver_id,
            action_type=f"APPROVAL_{decision}",
            payload={"request_id": request_id, "reasoning": reasoning},
            correlation_id=request_id
        )

        logger.info(f"Approval {request_id} resolved as {decision} by {approver_id}")
        return decision == "APPROVED"

approval_engine = ApprovalWorkflowEngine()
