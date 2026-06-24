from typing import Dict, Any
import logging
from datetime import datetime, timezone, timedelta
import uuid

from app.observability.metrics import metrics_store

logger = logging.getLogger(__name__)

class ContainmentEngine:
    """Orchestrates deterministic, reversible containment actions."""
    
    ALLOWED_ACTIONS = [
        "tighten_rate_limits",
        "websocket_quarantine",
        "temporary_tenant_isolation",
        "provider_circuit_escalation",
        "sync_pause",
        "degraded_mode_activation",
        "replay_invalidation"
    ]
    
    def trigger_containment(self, action_type: str, target_id: str, lineage_hash: str, enterprise_tenant: bool = False) -> Dict[str, Any]:
        """
        Triggers a deterministic containment action.
        Hard isolation for enterprise requires approval.
        """
        if action_type not in self.ALLOWED_ACTIONS:
            logger.error(f"Invalid containment action requested: {action_type}")
            return {"status": "FAILED", "reason": "invalid_action"}
            
        requires_approval = enterprise_tenant and action_type == "temporary_tenant_isolation"
        
        containment_record = {
            "action_id": f"cnt-{uuid.uuid4()}",
            "type": action_type,
            "target_id": target_id,
            "rollback_strategy": {"method": "revert_state", "target": target_id},
            "approval_required": requires_approval,
            "reversible_until": (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat(),
            "lineage_hash": lineage_hash,
            "status": "PENDING_APPROVAL" if requires_approval else "EXECUTED"
        }
        
        if not requires_approval:
            metrics_store.record_cyber_action("containment_actions_total")
            logger.warning(f"Autonomous containment executed: {action_type} on {target_id}")
            
        return containment_record

containment_engine = ContainmentEngine()
