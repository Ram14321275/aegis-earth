import pytest
from app.core.economics.stabilization.engine import economic_stabilization_engine

def test_stabilization_recommendation():
    res = economic_stabilization_engine.recommend_stabilization(supply_instability=0.9, logistics_congestion=0.8, market_volatility=0.95)
    types = [a["type"] for a in res["actions"]]
    assert "RELEASE_STRATEGIC_RESERVE" in types
    assert "FORCE_REROUTE_NON_ESSENTIAL" in types
    assert "ENACT_PRICE_CONTROLS" in types
    assert "reasoning_hash" in res
