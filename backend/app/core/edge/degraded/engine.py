from typing import Dict, Any
import logging

from app.core.edge.offline.queue import offline_queue
from app.observability.metrics import metrics_store

logger = logging.getLogger(__name__)

class DegradedModeEngine:
    """Activates offline operational continuity."""
    
    def activate_degraded_mode(self, node_id: str):
        metrics_store.record_edge_action("degraded_mode_activations_total")
        logger.warning(f"Edge Node {node_id} transitioned to DEGRADED MODE. Disconnected operations active.")

    def handle_degraded_operation(self, node_id: str, payload: Dict[str, Any]) -> bool:
        """Handles an operation strictly in offline mode."""
        logger.info(f"Processing local degraded operation for {node_id}")
        offline_queue.enqueue_event(node_id, payload)
        return True

degraded_engine = DegradedModeEngine()
