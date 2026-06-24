from typing import Dict, Any, List
import logging
import uuid
from datetime import datetime, timezone

from app.observability.metrics import metrics_store

logger = logging.getLogger(__name__)

class QuarantineManager:
    """Manages active quarantines and restrictions."""
    def __init__(self):
        self._active_quarantines: Dict[str, Dict[str, Any]] = {}

    def start_quarantine(self, target_id: str, reason: str) -> str:
        """Isolates a component temporarily."""
        session_id = f"qtn-{uuid.uuid4()}"
        self._active_quarantines[target_id] = {
            "session_id": session_id,
            "reason": reason,
            "start_time": datetime.now(timezone.utc)
        }
        metrics_store.record_cyber_action("quarantine_sessions_total")
        logger.warning(f"Quarantine started for {target_id}: {reason}")
        return session_id

    def is_quarantined(self, target_id: str) -> bool:
        return target_id in self._active_quarantines

    def lift_quarantine(self, target_id: str):
        """Reverses a quarantine action."""
        if target_id in self._active_quarantines:
            start_time = self._active_quarantines[target_id]["start_time"]
            duration = (datetime.now(timezone.utc) - start_time).total_seconds()
            metrics_store.record_cyber_action("quarantine_duration_seconds", duration)
            metrics_store.record_cyber_action("containment_rollbacks_total")
            
            del self._active_quarantines[target_id]
            logger.info(f"Quarantine lifted for {target_id}")

quarantine_manager = QuarantineManager()
