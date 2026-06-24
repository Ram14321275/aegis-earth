import pytest
from app.core.resilience.stabilization.engine import stabilization_engine

def test_stabilization_queue_pressure():
    res = stabilization_engine.generate_recommendations(15000, 1000, 0.5)
    assert res["stabilization_required"] is True
    assert "queue_pressure_stabilization" in res["recommended_actions"]
    assert "reasoning_hash" in res

def test_stabilization_healthy():
    res = stabilization_engine.generate_recommendations(100, 100, 0.1)
    assert res["stabilization_required"] is False
    assert len(res["recommended_actions"]) == 0
