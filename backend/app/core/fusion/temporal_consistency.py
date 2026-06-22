from typing import List, Dict, Any, Tuple
from datetime import datetime, timezone

class TemporalConsistencyEngine:
    """
    Prevents unstable intelligence oscillation (LOW <-> CRITICAL <-> LOW) using hysteresis.
    Applies time-decay weighting for older intelligence.
    """
    
    # Hysteresis Thresholds (0-100 scale)
    ESCALATION_THRESHOLD_DELTA = 15.0
    DE_ESCALATION_THRESHOLD_DELTA = 25.0 # Requires a larger drop to de-escalate

    def stabilize(self, current_score: float, historical_assessments: List[Dict[str, Any]]) -> Tuple[float, List[str]]:
        """
        Returns a stabilized score and a list of stabilization effects applied.
        """
        effects = []
        
        if not historical_assessments:
            return current_score, effects
            
        # Sort history by newest first
        sorted_history = sorted(historical_assessments, key=lambda x: x["timestamp"], reverse=True)
        previous_score = sorted_history[0].get("fused_score", current_score)
        
        delta = current_score - previous_score
        stabilized_score = current_score
        
        # 1. Hysteresis
        if delta > 0:
            # Escalating
            if delta < self.ESCALATION_THRESHOLD_DELTA:
                # Suppress minor noise spikes
                stabilized_score = previous_score
                effects.append(f"Suppressed minor escalation spike (+{delta:.1f} < {self.ESCALATION_THRESHOLD_DELTA})")
        elif delta < 0:
            # De-escalating
            if abs(delta) < self.DE_ESCALATION_THRESHOLD_DELTA:
                # Require significant evidence to de-escalate
                stabilized_score = previous_score
                effects.append(f"Suppressed minor de-escalation drop ({delta:.1f} > -{self.DE_ESCALATION_THRESHOLD_DELTA})")

        return stabilized_score, effects

    def calculate_time_decay_weight(self, timestamp: datetime) -> float:
        """
        Calculates a weight multiplier (0.0 to 1.0) based on age.
        Older intelligence decays in influence.
        """
        now = datetime.now(timezone.utc)
        age_hours = (now - timestamp).total_seconds() / 3600.0
        
        if age_hours <= 24:
            return 1.0
        elif age_hours <= 72:
            return 0.8
        elif age_hours <= 168: # 1 week
            return 0.5
        else:
            return 0.2

temporal_consistency_engine = TemporalConsistencyEngine()
