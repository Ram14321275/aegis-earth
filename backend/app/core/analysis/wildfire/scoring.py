from typing import Dict, Any, Tuple
from app.core.analysis.wildfire.models import WildfireRiskScore

class WildfireRiskScorer:
    @staticmethod
    def calculate_risk(
        total_burn_area_km2: float,
        high_extreme_burn_area_km2: float,
        vegetation_loss_percentage: float,
        confidence: float,
        days_since_acquisition: float
    ) -> Tuple[float, WildfireRiskScore]:
        """
        Determines the wildfire risk score (0-100) and severity using heuristic thresholds.
        """
        is_reliable = confidence > 0.5 and days_since_acquisition < 7.0
        
        # Calculate raw risk score (0-100)
        # Factor 1: High/Extreme Burn Area (weighted heavily)
        risk_score = 0.0
        
        if high_extreme_burn_area_km2 > 50.0:
            risk_score += 60.0
        elif high_extreme_burn_area_km2 > 10.0:
            risk_score += 40.0
        elif high_extreme_burn_area_km2 > 1.0:
            risk_score += 20.0
            
        # Factor 2: Total Burn Area
        if total_burn_area_km2 > 100.0:
            risk_score += 30.0
        elif total_burn_area_km2 > 20.0:
            risk_score += 15.0
        elif total_burn_area_km2 > 5.0:
            risk_score += 5.0
            
        # Factor 3: Vegetation Loss
        if vegetation_loss_percentage > 50.0:
            risk_score += 10.0
        elif vegetation_loss_percentage > 20.0:
            risk_score += 5.0
            
        # Cap score
        risk_score = min(100.0, risk_score)
        
        # Determine Severity Level based on Score
        if risk_score >= 75.0:
            severity = WildfireRiskScore.CRITICAL
        elif risk_score >= 50.0:
            severity = WildfireRiskScore.HIGH
        elif risk_score >= 25.0:
            severity = WildfireRiskScore.MODERATE
        else:
            severity = WildfireRiskScore.LOW
            
        # Downgrade if the data is heavily unreliable
        if not is_reliable:
            risk_score = risk_score * 0.8 # Reduce score by 20%
            if severity == WildfireRiskScore.CRITICAL:
                severity = WildfireRiskScore.HIGH
            elif severity == WildfireRiskScore.HIGH:
                severity = WildfireRiskScore.MODERATE
                
        return risk_score, severity
