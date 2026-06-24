from typing import Dict, Any, List
import logging
import hashlib
import uuid

logger = logging.getLogger(__name__)

class ResourceLineageTracker:
    """Tracks cryptographic lineage of economic disruptions and resource allocations."""
    
    def calculate_event_hash(self, event_type: str, resource_type: str, amount: float, parent_hash: str) -> str:
        """Deterministically hashes an economic event to preserve lineage."""
        payload = f"{event_type}|{resource_type}|{amount}|{parent_hash}"
        return hashlib.sha256(payload.encode()).hexdigest()
        
    def validate_lineage(self, lineage_chain: List[Dict[str, Any]]) -> bool:
        """Validates that a chain of economic events has not been tampered with."""
        for i in range(1, len(lineage_chain)):
            current = lineage_chain[i]
            parent = lineage_chain[i-1]
            
            # Recompute parent hash
            expected_parent_hash = self.calculate_event_hash(
                parent["event_type"], parent["resource_type"], parent["amount"], parent.get("parent_hash", "root")
            )
            
            if current["parent_hash"] != expected_parent_hash:
                logger.error(f"Economic lineage discontinuity detected between {parent['event_id']} and {current['event_id']}")
                return False
                
        return True

resource_lineage_tracker = ResourceLineageTracker()
