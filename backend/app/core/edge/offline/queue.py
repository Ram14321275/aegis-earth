from typing import Dict, Any, List
import logging
from datetime import datetime, timezone

from app.observability.metrics import metrics_store

logger = logging.getLogger(__name__)

class OfflineQueueManager:
    """Manages secure hazard queues during network partitions."""
    def __init__(self):
        self._queues: Dict[str, List[Dict[str, Any]]] = {} # node_id -> events

    def enqueue_event(self, node_id: str, event: Dict[str, Any]):
        """Queues an event locally for delayed synchronization."""
        if node_id not in self._queues:
            self._queues[node_id] = []
        
        # Ensure timestamp exists for future arbitration
        if "offline_timestamp" not in event:
            event["offline_timestamp"] = datetime.now(timezone.utc).isoformat()
            
        self._queues[node_id].append(event)
        metrics_store.record_edge_action("offline_queue_depth")
        logger.debug(f"Event queued offline for edge node {node_id}")

    def get_queued_events(self, node_id: str) -> List[Dict[str, Any]]:
        """Retrieves and clears the queue for synchronization."""
        events = self._queues.pop(node_id, [])
        return events

offline_queue = OfflineQueueManager()
