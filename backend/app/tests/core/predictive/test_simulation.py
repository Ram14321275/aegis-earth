import pytest
from app.core.predictive.simulation.engine import simulation_engine

@pytest.mark.asyncio
async def test_simulation_execution():
    sim = await simulation_engine.run_simulation("tenant_1", "wildfire_cascade", 72)
    assert sim.simulation_id is not None
    assert len(sim.cascades) > 0
    assert sim.explainability is not None
