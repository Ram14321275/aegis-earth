from typing import Dict, Any, List
import logging

from app.observability.metrics import metrics_store
from app.core.resilience.lineage.tracker import lineage_tracker
from app.core.resilience.telemetry.tracker import resilience_telemetry

logger = logging.getLogger(__name__)

class RecoveryVerificationEngine:
    """Fail-closed deterministic restoration verification."""
    
    def verify_restoration_chain(self, checkpoints: List[Dict[str, Any]], expected_region: str) -> bool:
        """Immediately aborts if any continuity or sovereign mismatches are detected."""
        
        # 1. Sovereign region mismatch
        for cp in checkpoints:
            if cp["region"] != expected_region:
                logger.error(f"Verification Abort: Sovereignty mismatch. Expected {expected_region}, got {cp['region']}")
                metrics_store.record_resilience_action("replay_verification_failures_total")
                resilience_telemetry.record_abort()
                return False
                
        # 2. Lineage Discontinuity
        if not lineage_tracker.validate_lineage(checkpoints):
            logger.error("Verification Abort: Lineage discontinuity or corruption detected.")
            metrics_store.record_resilience_action("replay_verification_failures_total")
            resilience_telemetry.record_abort()
            return False
            
        return True

verification_engine = RecoveryVerificationEngine()
