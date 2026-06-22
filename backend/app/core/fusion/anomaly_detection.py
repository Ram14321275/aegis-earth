import uuid
from typing import Dict, Any, Tuple
from datetime import datetime, timezone
from app.core.fusion.models import IntelligenceAnomaly

class AnomalyDetectionEngine:
    """
    Detects impossible jumps, invalid satellite deltas, or corrupted outputs.
    """
    
    def evaluate(self, current_score: float, previous_score: float, source_hazard_id: str) -> Tuple[bool, IntelligenceAnomaly | None]:
        """
        Returns (is_anomaly, anomaly_record)
        """
        delta = current_score - previous_score
        
        # 1. Impossible Jumps (e.g., 0 to 100 instantly with no intermediate scaling)
        if delta > 80.0:
            anomaly = IntelligenceAnomaly(
                anomaly_id=f"anom-{uuid.uuid4()}",
                source_hazard_id=source_hazard_id,
                anomaly_type="impossible_jump",
                details={"delta": delta, "current": current_score, "previous": previous_score},
                suppressed=True, # We suppress this intelligence
                timestamp=datetime.now(timezone.utc)
            )
            return True, anomaly
            
        # 2. Sudden Confidence Collapses (e.g. from 95 to 0 instantly)
        if delta < -80.0:
            anomaly = IntelligenceAnomaly(
                anomaly_id=f"anom-{uuid.uuid4()}",
                source_hazard_id=source_hazard_id,
                anomaly_type="sudden_collapse",
                details={"delta": delta, "current": current_score, "previous": previous_score},
                suppressed=True,
                timestamp=datetime.now(timezone.utc)
            )
            return True, anomaly
            
        return False, None

anomaly_detection_engine = AnomalyDetectionEngine()
