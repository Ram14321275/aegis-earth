import pytest
from app.core.predictive.forecasting.engine import forecasting_engine
from app.core.predictive.forecasting.models import ForecastWindow

@pytest.mark.asyncio
async def test_hazard_forecasting():
    forecast = await forecasting_engine.generate_forecast(
        "tenant_1", "wildfire", "region_x", ForecastWindow.TWENTY_FOUR_HOURS
    )
    assert forecast.forecast_id is not None
    assert forecast.explainability is not None
    assert len(forecast.explainability.contributing_factors) > 0
