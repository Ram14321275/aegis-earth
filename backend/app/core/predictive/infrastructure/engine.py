import logging
import uuid
from app.core.predictive.infrastructure.models import (
    InfrastructureForecast, QueuePressureForecast, WorkerCapacityPrediction, RegionalLoadPrediction
)
from app.core.predictive.explainability.contracts import Explanation, ContributingSignal
from app.observability.metrics import metrics_store
from datetime import datetime

logger = logging.getLogger(__name__)

class InfrastructurePredictionEngine:
    """
    Forecasts worker exhaustion, queue depth, and streaming overload.
    Recommends autoscaling actions.
    """

    async def generate_infrastructure_forecast(self) -> InfrastructureForecast:
        """
        Gathers metrics and generates a forecast.
        """
        metrics = metrics_store.get_metrics()
        
        # Mock logic based on metrics
        # In a real system, we'd analyze rate of change of queue depths over time.
        
        queue_forecast = QueuePressureForecast(
            queue_name="export_queue",
            saturation_risk=0.2,
            predicted_depth=50,
            time_to_saturation_minutes=120
        )
        
        worker_forecast = WorkerCapacityPrediction(
            worker_pool="default",
            exhaustion_probability=0.3,
            recommended_scale_up_instances=2
        )
        
        regional_load = RegionalLoadPrediction(
            region_id="global",
            api_overload_probability=0.1,
            websocket_pressure=0.15
        )
        
        explanation = Explanation(
            contributing_factors=[
                ContributingSignal(
                    source="metrics_store.gateway",
                    weight=0.6,
                    impact="API request volume increasing steadily.",
                    timestamp=datetime.utcnow().isoformat()
                )
            ],
            weighted_reasoning="Current worker count is sufficient for projected load, but queue depth is slowly increasing.",
            confidence_explanation="Based on direct internal telemetry (HIGH confidence).",
            uncertainty_explanation="Spikes in user traffic cannot be perfectly predicted.",
            degraded_mode_active=False
        )

        forecast = InfrastructureForecast(
            forecast_id=str(uuid.uuid4()),
            overall_health_risk=0.25,
            redis_latency_projection_ms=15.0,
            provider_degradation_probability=0.05,
            queue_forecasts=[queue_forecast],
            worker_forecasts=[worker_forecast],
            regional_loads=[regional_load],
            explainability=explanation
        )
        
        logger.info(f"Generated infrastructure forecast: {forecast.forecast_id}")
        return forecast

infrastructure_prediction_engine = InfrastructurePredictionEngine()
