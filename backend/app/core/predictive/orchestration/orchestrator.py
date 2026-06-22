import logging
from typing import Dict, Any

from app.core.predictive.forecasting.engine import forecasting_engine
from app.core.predictive.forecasting.models import ForecastWindow
from app.core.predictive.simulation.engine import simulation_engine
from app.core.predictive.infrastructure.engine import infrastructure_prediction_engine
from app.core.predictive.remediation.engine import autonomous_remediation_engine
from app.core.predictive.anomaly_detection.detector import anomaly_detector
from app.observability.metrics import metrics_store

logger = logging.getLogger(__name__)

class PredictiveOrchestrator:
    """
    Coordinates predictive engines, merges signals, and stabilizes conflicts.
    """

    async def run_predictive_cycle(self, tenant_id: str, hazard_type: str, region_id: str):
        """
        Runs a full predictive cycle.
        """
        logger.info(f"Starting predictive cycle for tenant {tenant_id}")
        
        # 1. Anomaly Detection
        anomalies = await anomaly_detector.detect_anomalies()
        
        # 2. Hazard Forecasting
        forecast = await forecasting_engine.generate_forecast(
            tenant_id=tenant_id,
            hazard_type=hazard_type,
            region_id=region_id,
            window=ForecastWindow.TWENTY_FOUR_HOURS
        )
        metrics_store.record_command_center_action("forecast_generation_total", 1)
        
        # 3. Infrastructure Prediction
        infra_forecast = await infrastructure_prediction_engine.generate_infrastructure_forecast()
        
        # 4. Autonomous Remediation
        remediation_plan = await autonomous_remediation_engine.evaluate_infrastructure_forecast(infra_forecast)
        if remediation_plan.decisions:
            metrics_store.record_command_center_action("autonomous_remediations_total", len(remediation_plan.decisions))
            
        # 5. Simulation (if needed, skipping automatic simulation for every cycle to save resources)
        # In a real system, we might only simulate if forecast severity is > 0.8
        
        return {
            "anomalies": anomalies,
            "forecast": forecast,
            "infrastructure": infra_forecast,
            "remediation_plan": remediation_plan
        }

    async def run_simulation(self, tenant_id: str, scenario: str, hours: int):
        """
        Triggers a planetary simulation.
        """
        return await simulation_engine.run_simulation(tenant_id, scenario, hours)

predictive_orchestrator = PredictiveOrchestrator()
