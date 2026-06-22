import pytest
from app.core.predictive.remediation.engine import autonomous_remediation_engine
from app.core.predictive.infrastructure.models import InfrastructureForecast, QueuePressureForecast
from app.core.predictive.explainability.contracts import Explanation
import uuid

@pytest.mark.asyncio
async def test_remediation_evaluation():
    # Mock high pressure queue
    qf = QueuePressureForecast(
        queue_name="test_queue",
        saturation_risk=0.5,
        predicted_depth=5000,
        time_to_saturation_minutes=10
    )
    
    infra = InfrastructureForecast(
        forecast_id=str(uuid.uuid4()),
        overall_health_risk=0.6,
        redis_latency_projection_ms=10.0,
        provider_degradation_probability=0.0,
        queue_forecasts=[qf],
        worker_forecasts=[],
        regional_loads=[],
        explainability=Explanation(
            contributing_factors=[], weighted_reasoning="", confidence_explanation="", uncertainty_explanation="", degraded_mode_active=False
        )
    )
    
    plan = await autonomous_remediation_engine.evaluate_infrastructure_forecast(infra)
    assert len(plan.decisions) == 1
    assert plan.decisions[0].recommended_workflow.steps[0].action_type == "SCALE_WORKERS"
    assert not plan.decisions[0].is_executed_automatically
