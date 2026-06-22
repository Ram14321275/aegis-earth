import logging

logger = logging.getLogger(__name__)

class ThreatPrioritizationEngine:
    """
    Deterministic prioritization using multiple explainable factors.
    Returns a score and an explanation of the calculation.
    """

    def calculate_priority(
        self,
        severity: float,
        confidence: float,
        population_exposed: int,
        is_fusion_event: bool,
        historical_persistence_hours: float
    ) -> tuple[float, str]:
        """
        Weights:
        - Severity: 40%
        - Population Exposure: 30%
        - Cross-hazard amplification (Fusion): 15%
        - Historical Persistence: 15%
        
        Confidence acts as a multiplier (0.0 to 1.0) to penalize low-reliability intelligence.
        """
        # Normalize population (assume 100k+ is max weight 1.0)
        pop_weight = min(population_exposed / 100000.0, 1.0)
        
        # Normalize persistence (assume 48h is max weight 1.0)
        persistence_weight = min(historical_persistence_hours / 48.0, 1.0)
        
        fusion_weight = 1.0 if is_fusion_event else 0.0

        base_score = (
            (severity * 0.40) +
            (pop_weight * 0.30) +
            (fusion_weight * 0.15) +
            (persistence_weight * 0.15)
        )

        final_score = base_score * confidence
        
        # Generate explainable rationale
        rationale = (
            f"Base Score: {base_score:.2f}. Multiplied by Confidence: {confidence:.2f} -> {final_score:.2f}. "
            f"Factors -> Severity: {severity:.2f}, Population Exposure: {population_exposed} (Wt: {pop_weight:.2f}), "
            f"Fusion Event: {is_fusion_event}, Persistence: {historical_persistence_hours}h (Wt: {persistence_weight:.2f})."
        )

        return final_score, rationale

threat_prioritization_engine = ThreatPrioritizationEngine()
