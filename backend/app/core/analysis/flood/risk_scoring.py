from typing import Dict, Any
from app.core.analysis.flood.models import FloodRiskScore

class RiskScorer:
    @staticmethod
    def calculate_risk(
        newly_inundated_area_km2: float,
        percentage_increase: float,
        confidence: float,
        cloud_cover: float,
        days_since_acquisition: float
    ) -> FloodRiskScore:
        """
        Determines the flood risk severity using heuristic thresholds.
        """
        # If confidence is extremely low or data is too old/cloudy, default to LOW or MODERATE based on area
        is_reliable = confidence > 0.5 and cloud_cover < 50.0 and days_since_acquisition < 7.0
        
        # Base severity derived strictly from newly inundated area and percentage increase
        if newly_inundated_area_km2 > 50.0 or percentage_increase > 100.0:
            severity = FloodRiskScore.CRITICAL
        elif newly_inundated_area_km2 > 10.0 or percentage_increase > 25.0:
            severity = FloodRiskScore.HIGH
        elif newly_inundated_area_km2 > 1.0 or percentage_increase > 5.0:
            severity = FloodRiskScore.MODERATE
        else:
            severity = FloodRiskScore.LOW
            
        # Downgrade if the data is heavily unreliable
        if not is_reliable:
            if severity == FloodRiskScore.CRITICAL:
                return FloodRiskScore.HIGH
            elif severity == FloodRiskScore.HIGH:
                return FloodRiskScore.MODERATE
                
        return severity
