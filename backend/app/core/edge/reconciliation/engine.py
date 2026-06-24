from typing import Dict, Any, List, Tuple
import uuid
import logging
from datetime import datetime, timezone

from app.core.edge.reconciliation.policies import ReconciliationPolicyEngine
from app.observability.metrics import metrics_store

logger = logging.getLogger(__name__)

class ConflictResolutionEngine:
    """Handles deterministic resolution of divergent edge states."""
    
    def __init__(self, policy_engine: ReconciliationPolicyEngine):
        self.policy_engine = policy_engine

    def resolve_divergence(self, base_state: Dict[str, Any], branch_a: Dict[str, Any], branch_b: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Deterministically resolves two conflicting branches originating from a base state.
        Returns the resolved state and the generated ReconciliationEvent metadata.
        """
        metrics_store.record_edge_action("reconciliation_conflicts_total")
        
        # Determine winning branch
        winning_state = self.policy_engine.resolve_timestamp_arbitration(branch_a, branch_b)
        
        reconciliation_id = f"rec-{uuid.uuid4()}"
        
        reconciliation_event = {
            "event_id": reconciliation_id,
            "type": "RECONCILIATION",
            "base_hash": base_state.get("payload_hash"),
            "branch_a_hash": branch_a.get("payload_hash"),
            "branch_b_hash": branch_b.get("payload_hash"),
            "resolved_hash": winning_state.get("payload_hash"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "policy_used": "timestamp_arbitration"
        }
        
        logger.info(f"Conflict resolved {reconciliation_id} - Branch hash selected: {winning_state.get('payload_hash')}")
        
        return winning_state, reconciliation_event

class LineageContinuityValidator:
    """Ensures deterministic replayability of reconciled events."""
    @staticmethod
    def is_lineage_intact(reconciliation_event: Dict[str, Any]) -> bool:
        """Verifies explicit merge lineage."""
        required = ["base_hash", "branch_a_hash", "branch_b_hash", "resolved_hash"]
        for key in required:
            if not reconciliation_event.get(key):
                return False
        return True

conflict_engine = ConflictResolutionEngine(ReconciliationPolicyEngine())
