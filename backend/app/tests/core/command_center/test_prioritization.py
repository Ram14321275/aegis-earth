import pytest
from app.core.command_center.prioritization.engine import threat_prioritization_engine

def test_prioritization_scoring():
    # High severity, max pop, max persistence, fusion event, high confidence
    score_high, rationale_high = threat_prioritization_engine.calculate_priority(
        severity=1.0,
        confidence=1.0,
        population_exposed=200000,
        is_fusion_event=True,
        historical_persistence_hours=72
    )
    # Score should be near 1.0
    assert score_high == 1.0

    # Low severity, low confidence
    score_low, rationale_low = threat_prioritization_engine.calculate_priority(
        severity=0.2,
        confidence=0.5,
        population_exposed=1000,
        is_fusion_event=False,
        historical_persistence_hours=1
    )
    assert score_low < 0.2
    assert "Multiplied by Confidence" in rationale_low
