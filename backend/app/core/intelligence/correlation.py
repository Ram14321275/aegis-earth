from typing import List

from app.core.intelligence.models import IntelligenceSignal, CorrelatedHazard
from app.domain.models.hazard import HazardType
from app.observability.metrics import metrics_store


class CrossHazardCorrelationEngine:
    @staticmethod
    def correlate(signals: List[IntelligenceSignal]) -> List[CorrelatedHazard]:
        """
        Applies deterministic rules to establish relationships between disparate hazard signals.
        For example: Wildfire + Vegetation Loss = High certainty of Cascading Burn Area.
        """
        correlations = []
        
        # Group signals by hazard type for faster lookup
        by_type = {}
        for s in signals:
            by_type.setdefault(s.hazard_type, []).append(s)
            
        wildfires = by_type.get(HazardType.WILDFIRE, [])
        veg_losses = by_type.get(HazardType.VEGETATION_LOSS, [])
        floods = by_type.get(HazardType.FLOOD, [])
        burn_changes = by_type.get(HazardType.ENVIRONMENTAL_CHANGE, []) # Represents temporal changes
        
        # Rule 1: Wildfire -> Vegetation Loss
        # If there's an active wildfire and historical veg loss/burn
        for w_sig in wildfires:
            for v_sig in veg_losses + burn_changes:
                # In a real spatial engine, we'd check ST_Intersects(w_sig.geom, v_sig.geom).
                # Here we assume they share the same context/location_id.
                correlations.append(
                    CorrelatedHazard(
                        primary_signal_id=w_sig.signal_id,
                        secondary_signal_id=v_sig.signal_id,
                        relationship_type="causes",
                        correlation_confidence=min(w_sig.confidence, v_sig.confidence),
                        description="Active wildfire is directly causing detected vegetation loss / burn scars."
                    )
                )
                
        # Rule 2: Vegetation Loss -> Flood Amplification
        for v_sig in veg_losses:
            for f_sig in floods:
                correlations.append(
                    CorrelatedHazard(
                        primary_signal_id=v_sig.signal_id,
                        secondary_signal_id=f_sig.signal_id,
                        relationship_type="amplifies",
                        correlation_confidence=min(v_sig.confidence, f_sig.confidence) * 0.9,
                        description="Prior vegetation loss reduces soil retention, amplifying current flood severity."
                    )
                )
                
        if correlations:
            metrics_store.record_correlation_event(len(correlations))
            
        return correlations

cross_hazard_correlation_engine = CrossHazardCorrelationEngine()
