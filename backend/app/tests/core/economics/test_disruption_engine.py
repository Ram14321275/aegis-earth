import pytest
from app.core.economics.disruption.engine import economic_disruption_engine

def test_disruption_scoring():
    res = economic_disruption_engine.calculate_disruption(root_cause_severity=0.8, dependencies=5)
    assert res["impact_score"] > 0.8
    assert res["cascading_depth"] == 5
    assert "reasoning_hash" in res

def test_minor_disruption():
    res = economic_disruption_engine.calculate_disruption(root_cause_severity=0.2, dependencies=4)
    assert res["impact_score"] == pytest.approx(0.28)
    assert res["cascading_depth"] == 2
