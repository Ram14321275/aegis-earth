import logging
import asyncio
from typing import List, Dict, Any
from app.core.fusion.reliability import reliability_engine
from app.core.fusion.anomaly_detection import anomaly_detection_engine
from app.core.fusion.temporal_consistency import temporal_consistency_engine
from app.core.fusion.correlation import correlation_engine
from app.core.fusion.fusion_engine import fusion_engine
from app.core.fusion.escalation import escalation_engine
from app.core.fusion.prioritization import operational_prioritization_engine
from app.core.fusion.geo_aggregation import geo_aggregation_engine

logger = logging.getLogger(__name__)

class FusionOrchestrator:
    """
    Coordinates the entire Multi-Region Intelligence Reliability & Disaster Fusion Pipeline.
    Fully asynchronous, non-blocking, and handles circuit protection (throttling).
    """
    
    def __init__(self):
        # Circuit Protection: Concurrency limit to prevent fusion storms
        self._semaphore = asyncio.Semaphore(50) 
        
    async def process_region(self, session: Any, lineage_id: str, correlation_id: str, raw_hazards: List[Dict[str, Any]], region_id: str):
        """
        Main pipeline flow:
        Hazard -> Reliability -> Anomaly -> Temporal -> Correlation -> Fusion -> Escalation -> Priority
        """
        async with self._semaphore:
            adjusted_hazards = []
            
            for raw in raw_hazards:
                hazard_id = raw.get("id", "unknown")
                raw_score = raw.get("risk_score", 0.0)
                metadata = raw.get("metadata", {})
                provider = raw.get("provider", "unknown")
                
                # 1. Reliability
                rel_assessment = reliability_engine.evaluate(raw_score, metadata, provider, hazard_id)
                
                # 2. Anomaly Detection
                # Requires mock historical fetch
                is_anomaly, anomaly_record = anomaly_detection_engine.evaluate(rel_assessment.reliability_adjusted_score, previous_score=0.0, source_hazard_id=hazard_id)
                if is_anomaly and anomaly_record.suppressed:
                    logger.warning(f"Anomaly detected and suppressed for hazard {hazard_id}")
                    continue
                    
                # 3. Temporal Consistency
                # Requires mock historical fetch
                stabilized_score, effects = temporal_consistency_engine.stabilize(rel_assessment.reliability_adjusted_score, [])
                
                # Store adjusted data
                adjusted_hazards.append({
                    "hazard_type": raw.get("hazard_type"),
                    "reliability_adjusted_score": stabilized_score,
                    "provider_degraded": rel_assessment.provider_degraded
                })
                
            # 4. Correlation (Cascading)
            cascades = await correlation_engine.detect_cascades(session, "ANY", "any_id", adjusted_hazards, region_id)
            
            # 5. Fusion
            fused_assessment = fusion_engine.execute_fusion(lineage_id, correlation_id, adjusted_hazards, region_id, "local")
            
            # 6. Escalation
            active_cascade_ids = [c.correlation_event_id for c in cascades]
            escalation = escalation_engine.evaluate(fused_assessment.fused_score, fused_assessment.threat_level, active_cascade_ids, region_id, "fused_id")
            
            # 7. Prioritization
            if escalation:
                priority_score = operational_prioritization_engine.calculate_priority(
                    escalation_level=escalation.escalation_level,
                    fused_score=fused_assessment.fused_score,
                    population_impacted=10000, # Mock
                    active_queue_depth=10,
                    available_workers=5
                )
                logger.info(f"Generated Escalation: {escalation.escalation_level} with priority {priority_score}")
                
            # 8. Streaming + Persistence (Deferred to outside logic / repositories)
            
            return fused_assessment

fusion_orchestrator = FusionOrchestrator()
