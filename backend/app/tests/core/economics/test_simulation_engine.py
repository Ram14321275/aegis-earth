import pytest
from app.core.economics.simulation.engine import economic_simulation_engine

@pytest.mark.asyncio
async def test_economic_simulation():
    res = await economic_simulation_engine.run_simulation("global_shipping_collapse", {})
    assert res["status"] == "COMPLETED"
    assert res["production_impact"] is False
    assert res["results"]["collapse_probability"] == 0.85

@pytest.mark.asyncio
async def test_invalid_economic_simulation():
    res = await economic_simulation_engine.run_simulation("alien_invasion", {})
    assert res["status"] == "FAILED"
