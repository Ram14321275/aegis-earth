import time
from typing import List

from app.core.intelligence.models import IntelligenceSignal, PrioritizedEvent
from app.schemas.intelligence import SeverityEnum
from app.observability.metrics import metrics_store


class EventPrioritizationEngine:
    @staticmethod
    def _get_severity_weight(severity: SeverityEnum) -> float:
        weights = {
            SeverityEnum.CRITICAL: 100.0,
            SeverityEnum.HIGH: 75.0,
            SeverityEnum.MEDIUM: 50.0,
            SeverityEnum.LOW: 25.0
        }
        return weights.get(severity, 0.0)

    @staticmethod
    def prioritize(signals: List[IntelligenceSignal]) -> List[PrioritizedEvent]:
        """
        Ranks incoming intelligence signals based on severity, confidence, and spatial scale.
        """
        start_time = time.time()
        
        try:
            prioritized = []
            
            for signal in signals:
                # 1. Base score from semantic severity
                severity_score = EventPrioritizationEngine._get_severity_weight(signal.severity)
                
                # 2. Modulate by raw intensity (how rapidly changing or severe the anomaly is natively)
                # raw_score is 0-100. We blend it.
                intensity_score = (severity_score * 0.7) + (signal.raw_score * 0.3)
                
                # 3. Apply confidence multiplier
                confidence_adjusted = intensity_score * signal.confidence
                
                # 4. Area multiplier (logarithmic scale to prevent massive barren areas from always winning)
                import math
                area_multiplier = 1.0 + (math.log10(signal.affected_area_km2 + 1.0) / 10.0)
                
                final_priority = min(100.0, confidence_adjusted * area_multiplier)
                
                prioritized.append({
                    "signal": signal,
                    "score": final_priority
                })
                
            # Sort descending
            prioritized.sort(key=lambda x: x["score"], reverse=True)
            
            results = []
            for rank, item in enumerate(prioritized, start=1):
                results.append(
                    PrioritizedEvent(
                        signal=item["signal"],
                        priority_score=item["score"],
                        priority_rank=rank
                    )
                )
                
            return results
        finally:
            duration_ms = (time.time() - start_time) * 1000.0
            metrics_store.record_prioritization_duration(duration_ms)

event_prioritization_engine = EventPrioritizationEngine()
