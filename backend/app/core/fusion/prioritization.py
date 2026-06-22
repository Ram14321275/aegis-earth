class OperationalPrioritizationEngine:
    """
    Calculates dynamic priority score considering hazard severity, 
    human/infrastructure risk, operational queue saturation, and worker availability.
    """
    
    def calculate_priority(
        self, 
        escalation_level: str, 
        fused_score: float, 
        population_impacted: int, 
        active_queue_depth: int, 
        available_workers: int
    ) -> float:
        
        priority = 0.0
        
        # 1. Base Priority by Escalation Level
        level_weights = {
            "catastrophic": 50.0,
            "emergency": 40.0,
            "severe": 30.0,
            "elevated": 20.0,
            "advisory": 10.0
        }
        priority += level_weights.get(escalation_level, 0.0)
        
        # 2. Add fused risk intensity (scaled to max 20)
        priority += (fused_score * 0.2)
        
        # 3. Add population impact (logarithmic scaling, max 20)
        if population_impacted > 1000000:
            priority += 20.0
        elif population_impacted > 100000:
            priority += 15.0
        elif population_impacted > 10000:
            priority += 10.0
        elif population_impacted > 1000:
            priority += 5.0
            
        # 4. Apply Operational Capacity Constraints
        # If the queue is saturated, we must heavily penalize new non-critical events
        saturation_ratio = active_queue_depth / (available_workers * 10) if available_workers > 0 else 1.0
        
        if saturation_ratio > 0.8 and escalation_level not in ["catastrophic", "emergency"]:
            # Suppress priority of minor events during global congestion
            priority *= 0.5
            
        return min(100.0, max(0.0, priority))

operational_prioritization_engine = OperationalPrioritizationEngine()
