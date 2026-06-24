from typing import Dict, Any, List
import logging
import hashlib

logger = logging.getLogger(__name__)

class RecoveryLineageTracker:
    """Tracks and validates immutable recovery chains."""
    
    def calculate_checkpoint_hash(self, snapshot_hash: str, orchestration_hash: str, tenant_id: str, region: str) -> str:
        """Deterministically hashes checkpoint variables."""
        payload = f"{snapshot_hash}|{orchestration_hash}|{tenant_id}|{region}"
        return hashlib.sha256(payload.encode()).hexdigest()
        
    def validate_lineage(self, checkpoints: List[Dict[str, Any]]) -> bool:
        """Validates that a chain of checkpoints has not been tampered with or corrupted."""
        for i in range(1, len(checkpoints)):
            current = checkpoints[i]
            parent = checkpoints[i-1]
            
            # The parent_hash of the current must match the computed hash of the parent
            expected_parent_hash = self.calculate_checkpoint_hash(
                parent["snapshot_hash"], parent["orchestration_hash"], parent["tenant_id"], parent["region"]
            )
            
            if current["parent_checkpoint_hash"] != expected_parent_hash:
                logger.error(f"Lineage discontinuity detected between {parent['checkpoint_id']} and {current['checkpoint_id']}")
                return False
                
        return True

lineage_tracker = RecoveryLineageTracker()
