import pytest
from app.core.economics.forecasting.engine import economic_forecasting_engine

def test_shortfall_forecast():
    res = economic_forecasting_engine.generate_shortfall_forecast("energy", current_stock=100.0, consumption_rate=50.0, inbound_supply=10.0)
    assert res["resource_type"] == "energy"
    # Net daily: -40. Over 30 days: -1200. Plus stock (100): -1100 => shortfall is 1100
    assert res["projected_shortfall"] == 1100.0
    assert "reasoning_hash" in res

def test_healthy_forecast():
    res = economic_forecasting_engine.generate_shortfall_forecast("energy", current_stock=1000.0, consumption_rate=10.0, inbound_supply=20.0)
    assert res["projected_shortfall"] == 0.0
