import uuid
from typing import List, Dict, Any
from datetime import datetime, timezone
from app.core.fusion.models import RegionalThreatAssessment, FusionExplanation, AggregationHierarchy

class FusionEngine:
    """
    Fuses multiple reliability-adjusted hazards into a coherent Regional Threat Assessment.
    Provides mathematically sound Explainability outputs and degrades gracefully.
    """
    
    def execute_fusion(
        self, 
        lineage_id: str, 
        correlation_id: str, 
        adjusted_hazards: List[Dict[str, Any]], 
        region_id: str, 
        aggregation_level: str
    ) -> RegionalThreatAssessment:
        
        weights = {}
        contributing_hazards = []
        suppression_reasons = []
        
        fused_score = 0.0
        max_score = 0.0
        
        # Graceful degradation logic
        valid_hazards = [h for h in adjusted_hazards if not h.get("provider_degraded", False)]
        
        if not valid_hazards:
            suppression_reasons.append("All contributing hazards were flagged as degraded.")
            # If everything failed, we return a degraded 0 score
            return self._build_empty_assessment(lineage_id, correlation_id, region_id, aggregation_level, suppression_reasons)

        for hz in valid_hazards:
            score = hz.get("reliability_adjusted_score", 0.0)
            hazard_type = hz.get("hazard_type", "unknown")
            
            contributing_hazards.append(hazard_type)
            weights[hazard_type] = score
            
            fused_score += score
            if score > max_score:
                max_score = score
                
        # Fusion math: We don't just sum them (that could exceed 100 easily).
        # We take the maximum threat, and then add a fractional penalty for compounding secondary threats.
        compound_penalty = (fused_score - max_score) * 0.2
        final_fused_score = min(100.0, max_score + compound_penalty)
        
        threat_level = self._determine_threat_level(final_fused_score)
        
        explanation = FusionExplanation(
            reasoning_summary=f"Fused maximum threat of {max_score:.1f} with compounding penalty +{compound_penalty:.1f}",
            contributing_hazards=contributing_hazards,
            weights=weights,
            suppression_reasons=suppression_reasons,
            temporal_stabilization_effects=[]
        )
        
        hierarchy = AggregationHierarchy(
            level=aggregation_level,
            region_id=region_id
        )

        return RegionalThreatAssessment(
            lineage_id=lineage_id,
            correlation_id=correlation_id,
            aggregation_hierarchy=hierarchy,
            fused_score=final_fused_score,
            threat_level=threat_level,
            explanation=explanation,
            event_version=1,
            timestamp=datetime.now(timezone.utc)
        )
        
    def _determine_threat_level(self, score: float) -> str:
        if score >= 80.0:
            return "CRITICAL"
        if score >= 60.0:
            return "HIGH"
        if score >= 30.0:
            return "MODERATE"
        return "LOW"
        
    def _build_empty_assessment(self, lineage_id: str, correlation_id: str, region_id: str, aggregation_level: str, suppression_reasons: List[str]) -> RegionalThreatAssessment:
        explanation = FusionExplanation(
            reasoning_summary="Fusion failed or fully degraded.",
            contributing_hazards=[],
            weights={},
            suppression_reasons=suppression_reasons
        )
        hierarchy = AggregationHierarchy(level=aggregation_level, region_id=region_id)
        return RegionalThreatAssessment(
            lineage_id=lineage_id,
            correlation_id=correlation_id,
            aggregation_hierarchy=hierarchy,
            fused_score=0.0,
            threat_level="LOW",
            explanation=explanation,
            event_version=1,
            timestamp=datetime.now(timezone.utc)
        )

fusion_engine = FusionEngine()
