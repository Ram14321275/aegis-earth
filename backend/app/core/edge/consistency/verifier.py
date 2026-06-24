from typing import List, Dict, Any
import logging

from app.observability.metrics import metrics_store

logger = logging.getLogger(__name__)

class ConsistencyVerifier:
    """Validates lineage continuity and synchronization state."""
    
    @staticmethod
    def verify_lineage(events: List[Dict[str, Any]]) -> bool:
        """Detects lineage gaps and replay divergence."""
        if not events:
            return True
            
        for i in range(1, len(events)):
            current = events[i]
            parent = events[i - 1]
            
            # Check chained lineage
            if current.get("parent_event_id") != parent.get("event_id"):
                logger.error(f"Consistency Violation: Lineage gap detected between {parent.get('event_id')} and {current.get('event_id')}")
                metrics_store.record_edge_action("consistency_violations_total")
                metrics_store.record_edge_action("lineage_divergence_total")
                return False
                
        return True

consistency_verifier = ConsistencyVerifier()
