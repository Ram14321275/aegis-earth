import pytest
from app.core.cyber.simulation.engine import simulation_engine

@pytest.mark.asyncio
async def test_cyber_simulation():
    res = await simulation_engine.run_simulation("ddos_simulation", {"intensity": "high"})
    assert res["status"] == "COMPLETED"
    assert res["scenario"] == "ddos_simulation"
    assert res["production_impact"] is False
    
@pytest.mark.asyncio
async def test_invalid_cyber_simulation():
    res = await simulation_engine.run_simulation("unknown_hack", {})
    assert res["status"] == "FAILED"
