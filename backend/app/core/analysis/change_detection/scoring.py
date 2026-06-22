from typing import Tuple

from app.core.analysis.change_detection.models import (
    ChangeMetrics, EnvironmentalRiskCategory, ChangeDirection
)


class EnvironmentalChangeScorer:
    @staticmethod
    def calculate_risk(metrics: ChangeMetrics, confidence: float) -> Tuple[float, EnvironmentalRiskCategory, bool]:
        """
        Interprets raw spectral deltas to compute a semantic 0-100 risk score.
        High scores indicate severe, rapid, or critical environmental shifts (e.g., massive vegetation loss).
        """
        base_score = 0.0
        
        # We consider LOSS in vegetation/water and GAIN in urban/burn as "risk-increasing" changes.
        # Vegetation loss increases risk
        if metrics.ndvi_delta.direction == ChangeDirection.LOSS:
            base_score += min(50.0, metrics.ndvi_delta.significant_change_area_km2 * 2.0)
            
        # Water loss increases risk
        if metrics.ndwi_delta.direction == ChangeDirection.LOSS:
            base_score += min(30.0, metrics.ndwi_delta.significant_change_area_km2 * 1.5)
            
        # Burn gain (high NBR drop) increases risk
        if metrics.nbr_delta.direction == ChangeDirection.LOSS:  # NBR loss means burn
            base_score += min(40.0, metrics.nbr_delta.significant_change_area_km2 * 3.0)
            
        # Urban gain increases risk
        if metrics.ndbi_delta.direction == ChangeDirection.GAIN:
            base_score += min(30.0, metrics.ndbi_delta.significant_change_area_km2 * 1.0)
            
        # Cap base score
        raw_score = min(100.0, base_score)
        
        # Apply confidence downgrade (e.g., if there's high cloud variance)
        # Assuming confidence is [0, 1]
        final_score = raw_score * confidence
        
        if final_score >= 75.0:
            category = EnvironmentalRiskCategory.CRITICAL_CHANGE
        elif final_score >= 50.0:
            category = EnvironmentalRiskCategory.HIGH_CHANGE
        elif final_score >= 25.0:
            category = EnvironmentalRiskCategory.MODERATE_CHANGE
        else:
            category = EnvironmentalRiskCategory.STABLE
            
        # A change is alertable if it's severe and we have high confidence.
        # Non-dangerous or long-term trends shouldn't necessarily spam alerts unless critical.
        alertable = final_score >= 50.0 and confidence >= 0.7
        
        return final_score, category, alertable
