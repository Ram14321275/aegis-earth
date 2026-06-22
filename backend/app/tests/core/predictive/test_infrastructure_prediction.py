import pytest
from app.core.predictive.infrastructure.engine import infrastructure_prediction_engine

@pytest.mark.asyncio
async def test_infrastructure_forecast():
    infra = await infrastructure_prediction_engine.generate_infrastructure_forecast()
    assert infra.forecast_id is not None
    assert len(infra.queue_forecasts) > 0
