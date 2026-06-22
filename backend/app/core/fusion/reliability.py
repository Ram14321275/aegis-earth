import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List
from app.core.fusion.models import ReliabilityAssessment

class ReliabilityEngine:
    """
    Measures trustworthiness of intelligence outputs without mutating raw scores.
    Detects provider drift and applies penalties for stale data or cloud cover.
    """
    
    def evaluate(self, raw_score: float, metadata: Dict[str, Any], provider_source: str, source_hazard_id: str) -> ReliabilityAssessment:
        now = datetime.now(timezone.utc)
        degradation_reasons = []
        
        # Base reliability
        reliability_score = 1.0
        
        # 1. Cloud Coverage Penalty
        cloud_coverage = metadata.get("cloud_coverage", 0.0)
        if cloud_coverage > 20.0:
            penalty = min((cloud_coverage - 20.0) * 0.01, 0.4) # max 40% penalty
            reliability_score -= penalty
            degradation_reasons.append(f"High cloud coverage: {cloud_coverage}%")
            
        # 2. Stale Imagery Penalty
        days_stale = metadata.get("days_stale", 0)
        if days_stale > 3:
            penalty = min((days_stale - 3) * 0.05, 0.5) # max 50% penalty
            reliability_score -= penalty
            degradation_reasons.append(f"Stale imagery: {days_stale} days old")
            
        # 3. Provider Drift Detection
        provider_degraded = False
        drift_factor = metadata.get("provider_inconsistency_flags", 0)
        if drift_factor > 2:
            reliability_score -= 0.3
            provider_degraded = True
            degradation_reasons.append("Provider drift detected: conflicting temporal outputs")
            
        # Ensure bounds
        reliability_score = max(0.0, min(1.0, reliability_score))
        
        # Calculate Reliability Adjusted Score
        # E.g. A score of 82 with 0.8 reliability -> might just be reported alongside, or mathematically adjusted
        # The user requested: "preserve original hazard scores, attach reliability modifiers separately"
        reliability_adjusted_score = raw_score * reliability_score
        
        return ReliabilityAssessment(
            snapshot_id=f"rel-{uuid.uuid4()}",
            source_hazard_id=source_hazard_id,
            raw_score=raw_score,
            reliability_adjusted_score=reliability_adjusted_score,
            reliability_score=reliability_score * 100.0, # scaled to 0-100
            provider_source=provider_source,
            provider_degraded=provider_degraded,
            degradation_reasons=degradation_reasons,
            timestamp=now
        )

reliability_engine = ReliabilityEngine()
