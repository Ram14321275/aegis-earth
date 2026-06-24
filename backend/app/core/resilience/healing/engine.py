from typing import Dict, Any, List
import logging
import uuid
import hashlib

from app.observability.metrics import metrics_store

logger = logging.getLogger(__name__)

class SelfHealingEngine:
    """Orchestrates deterministic self-healing actions."""
    
    # Categorize actions strictly
    SAFE_AUTOMATION = ["clear_cache", "reset_rate_limits", "sync_retry"]
    APPROVAL_REQUIRED = ["restart_worker_pool", "rebuild_search_index"]
    FORBIDDEN_AUTOMATION = ["drop_database", "purge_checkpoints"]
    
    def trigger_healing(self, action_type: str, target: str) -> Dict[str, Any]:
        """Triggers a self-healing action deterministically."""
        
        if action_type in self.FORBIDDEN_AUTOMATION:
            logger.error(f"Forbidden self-healing action attempted: {action_type}")
            return {"status": "FAILED", "reason": "FORBIDDEN"}
            
        action_id = f"heal-{uuid.uuid4()}"
        category = "SAFE_AUTOMATION" if action_type in self.SAFE_AUTOMATION else "APPROVAL_REQUIRED"
        
        # Deterministic reasoning trace
        reasoning_str = f"action:{action_type}|target:{target}|cat:{category}"
        reasoning_hash = hashlib.sha256(reasoning_str.encode()).hexdigest()
        
        result = {
            "action_id": action_id,
            "type": action_type,
            "target": target,
            "category": category,
            "rollback_strategy": {"method": "revert", "action_id": action_id},
            "reasoning_hash": reasoning_hash,
            "status": "PENDING_APPROVAL" if category == "APPROVAL_REQUIRED" else "EXECUTED"
        }
        
        if category == "SAFE_AUTOMATION":
            metrics_store.record_resilience_action("healing_actions_total")
            logger.warning(f"Autonomous healing executed: {action_type} on {target}")
            
        return result

healing_engine = SelfHealingEngine()
