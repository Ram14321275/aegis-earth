from typing import Dict, Optional
import uuid
import logging

logger = logging.getLogger(__name__)

class CheckpointManager:
    def __init__(self):
        # Simulated DB store
        self._checkpoints: Dict[str, str] = {} # node_id -> last_event_id

    def update_checkpoint(self, node_id: str, last_event_id: str):
        """Deterministically tracks synchronization progress."""
        self._checkpoints[node_id] = last_event_id
        logger.debug(f"Updated synchronization checkpoint for {node_id} to {last_event_id}")

    def get_checkpoint(self, node_id: str) -> Optional[str]:
        return self._checkpoints.get(node_id)

checkpoint_manager = CheckpointManager()
