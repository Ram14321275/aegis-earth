import uuid
from typing import Optional, List
from datetime import datetime, timezone
from app.core.fusion.models import EscalationEvent

class EscalationEngine:
    """
    Evaluates fused assessments and cascading risks to generate System Escalation events.
    Escalation levels: advisory, elevated, severe, emergency, catastrophic
    """
    
    def evaluate(self, fused_score: float, threat_level: str, active_cascades: List[str], region_id: str, fused_assessment_id: str) -> Optional[EscalationEvent]:
        
        # 1. Catastrophic: Critical + multiple interacting cascades
        if fused_score >= 95.0 and len(active_cascades) >= 2:
            return self._build_event("catastrophic", "Compound disaster threshold exceeded (CRITICAL score + 2 interacting cascades)", region_id, fused_assessment_id)
            
        # 2. Emergency: Critical hazard
        if threat_level == "CRITICAL" or fused_score >= 85.0:
            return self._build_event("emergency", "Critical regional threat level breached", region_id, fused_assessment_id)
            
        # 3. Severe: High threat + active cascade
        if threat_level == "HIGH" and len(active_cascades) >= 1:
            return self._build_event("severe", "High threat amplified by cascading interaction", region_id, fused_assessment_id)
            
        # 4. Elevated: High threat without active cascades
        if threat_level == "HIGH":
            return self._build_event("elevated", "High threat condition active", region_id, fused_assessment_id)
            
        # 5. Advisory: Moderate threat
        if threat_level == "MODERATE":
            return self._build_event("advisory", "Moderate threat conditions monitored", region_id, fused_assessment_id)
            
        return None
        
    def _build_event(self, level: str, reason: str, region_id: str, fused_assessment_id: str) -> EscalationEvent:
        return EscalationEvent(
            escalation_id=f"esc-{uuid.uuid4()}",
            region_id=region_id,
            escalation_level=level,
            trigger_reason=reason,
            fused_assessment_id=fused_assessment_id,
            timestamp=datetime.now(timezone.utc)
        )

escalation_engine = EscalationEngine()
