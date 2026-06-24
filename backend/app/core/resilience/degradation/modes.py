from typing import Dict, Any
import logging

from app.observability.metrics import metrics_store

logger = logging.getLogger(__name__)

class DegradationManager:
    """Manages graceful continuity modes during planetary disaster scenarios."""
    
    ALLOWED_MODES = [
        "READ_ONLY",
        "CACHE_ONLY",
        "OFFLINE_EDGE",
        "TELEMETRY_ONLY",
        "EMERGENCY_COORDINATION",
        "NORMAL"
    ]
    
    def __init__(self):
        self._current_mode = "NORMAL"
        
    def transition_mode(self, new_mode: str) -> bool:
        if new_mode not in self.ALLOWED_MODES:
            logger.error(f"Attempted to transition to invalid degradation mode: {new_mode}")
            return False
            
        if self._current_mode != new_mode:
            logger.critical(f"System degraded mode transitioning: {self._current_mode} -> {new_mode}")
            self._current_mode = new_mode
            if new_mode != "NORMAL":
                metrics_store.record_resilience_action("degraded_mode_activations_total")
                
        return True
        
    def get_current_mode(self) -> str:
        return self._current_mode

degradation_manager = DegradationManager()
