from typing import Dict, Any, Optional
import logging
import uuid
import hashlib

from app.observability.metrics import metrics_store
from app.core.resilience.sovereignty.fencing import sovereign_fencing

logger = logging.getLogger(__name__)

class FailoverPromoter:
    """Handles sovereign failover orchestration and split-brain prevention."""
    
    def __init__(self):
        self._current_primary = "node-us-east-1"
        self._fencing_token = 1
        
    def promote_node(self, old_primary: str, new_primary: str, primary_region: str, new_region: str) -> Dict[str, Any]:
        """Promotes a new primary deterministically."""
        
        if not sovereign_fencing.validate_failover_region(primary_region, new_region):
            return {"status": "FAILED", "reason": "SOVEREIGNTY_VIOLATION"}
            
        # Monotonic generation counter (split-brain prevention)
        self._fencing_token += 1
        
        reasoning = f"old:{old_primary}|new:{new_primary}|token:{self._fencing_token}"
        reasoning_hash = hashlib.sha256(reasoning.encode()).hexdigest()
        
        self._current_primary = new_primary
        metrics_store.record_resilience_action("failover_promotions_total")
        
        logger.warning(f"Failover executed. {new_primary} is now PRIMARY (token {self._fencing_token})")
        
        return {
            "status": "PROMOTED",
            "new_primary": new_primary,
            "fencing_token": self._fencing_token,
            "reasoning_hash": reasoning_hash
        }

failover_promoter = FailoverPromoter()
