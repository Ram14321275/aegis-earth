import pytest
from app.core.economics.logistics.router import logistics_router

def test_logistics_routing():
    res = logistics_router.calculate_corridor("NYC", "LON", 0.9)
    assert res["reroute_recommended"] is True
    assert res["congestion_score"] == 0.9
    assert "reasoning_hash" in res

def test_logistics_routing_healthy():
    res = logistics_router.calculate_corridor("NYC", "LON", 0.4)
    assert res["reroute_recommended"] is False
