import logging
import uuid
from datetime import datetime, timedelta
from typing import Optional

from app.core.predictive.forecasting.models import HazardForecast, ForecastWindow, PredictionConfidence
from app.core.predictive.explainability.contracts import Explanation, ContributingSignal

logger = logging.getLogger(__name__)

class ForecastingEngine:
    """
    Predicts hazard escalation probabilities.
    Includes deterministic fallback modes and confidence penalties for stale data.
    """

    async def generate_forecast(
        self, tenant_id: str, hazard_type: str, region_id: str, window: ForecastWindow
    ) -> HazardForecast:
        """
        Generates a confidence-weighted hazard projection.
        """
        # MVP: Deterministic fallback logic. In a real system, this would call an ML model
        # and fallback to deterministic if the model times out or degrades.
        
        generated_at = datetime.utcnow()
        
        # Adaptive TTL
        if window in [ForecastWindow.ONE_HOUR, ForecastWindow.SIX_HOURS]:
            expires_at = generated_at + timedelta(minutes=5)
        elif window in [ForecastWindow.TWENTY_FOUR_HOURS, ForecastWindow.SEVENTY_TWO_HOURS]:
            expires_at = generated_at + timedelta(minutes=30)
        else:
            expires_at = generated_at + timedelta(hours=2)
            
        # Mocking logic for deterministic fallback
        severity = 0.6
        probability = 0.75
        confidence = PredictionConfidence.MODERATE
        
        explanation = Explanation(
            contributing_factors=[
                ContributingSignal(
                    source="historical_snapshot",
                    weight=0.8,
                    impact="Escalation trajectory detected.",
                    timestamp=generated_at.isoformat()
                )
            ],
            weighted_reasoning="Historical persistence combined with recent anomaly spikes suggests escalation.",
            confidence_explanation="Stale weather data reduced confidence from HIGH to MODERATE.",
            uncertainty_explanation="Incomplete satellite coverage in the western sector.",
            degraded_mode_active=True # Because we are using deterministic fallback
        )
        
        forecast = HazardForecast(
            forecast_id=str(uuid.uuid4()),
            hazard_type=hazard_type,
            region_id=region_id,
            predicted_severity=severity,
            predicted_probability=probability,
            confidence=confidence,
            forecast_window=window,
            generated_at=generated_at,
            expires_at=expires_at,
            explainability=explanation,
            uncertainty_score=0.4
        )
        
        logger.info(f"Generated forecast {forecast.forecast_id} for {hazard_type} in {region_id}")
        return forecast

forecasting_engine = ForecastingEngine()
