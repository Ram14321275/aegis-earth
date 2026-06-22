import pytest
from datetime import datetime, timezone
import pytest_asyncio
from app.core.fusion.reliability import reliability_engine
from app.core.fusion.temporal_consistency import temporal_consistency_engine
from app.core.fusion.anomaly_detection import anomaly_detection_engine
from app.core.fusion.escalation import escalation_engine
from app.core.fusion.prioritization import operational_prioritization_engine
from app.core.fusion.correlation import correlation_engine
from app.core.fusion.fusion_engine import fusion_engine
from app.core.fusion.geo_aggregation import geo_aggregation_engine

def test_reliability_degradation():
    """Test that cloud cover and stale imagery gracefully degrade raw scores."""
    raw_score = 80.0
    metadata = {"cloud_coverage": 40.0, "days_stale": 5}
    assessment = reliability_engine.evaluate(raw_score, metadata, "mock_provider", "hazard-1")
    
    assert assessment.raw_score == 80.0
    # 40% cloud = 20% penalty. 5 days stale = 10% penalty. Total 30% penalty. Reliability = 0.7.
    assert assessment.reliability_score == pytest.approx(70.0)
    assert assessment.reliability_adjusted_score == pytest.approx(56.0) # 80 * 0.7
    assert len(assessment.degradation_reasons) == 2

def test_anomaly_suppression():
    """Test impossible jumps are flagged and suppressed."""
    current = 90.0
    previous = 5.0
    is_anomaly, record = anomaly_detection_engine.evaluate(current, previous, "hazard-1")
    assert is_anomaly
    assert record.anomaly_type == "impossible_jump"
    assert record.suppressed is True

def test_temporal_hysteresis():
    """Test hysteresis thresholds suppress minor noise."""
    history = [{"fused_score": 50.0, "timestamp": datetime.now(timezone.utc)}]
    
    # 1. Minor escalation (+10) -> Should be suppressed back to 50
    stable, effects = temporal_consistency_engine.stabilize(60.0, history)
    assert stable == 50.0
    assert "Suppressed minor escalation spike" in effects[0]
    
    # 2. Major escalation (+20) -> Should pass through
    stable2, _ = temporal_consistency_engine.stabilize(70.0, history)
    assert stable2 == 70.0
    
    # 3. Minor de-escalation (-20) -> Should be suppressed (requires > 25 drop)
    history2 = [{"fused_score": 80.0, "timestamp": datetime.now(timezone.utc)}]
    stable3, effects3 = temporal_consistency_engine.stabilize(60.0, history2)
    assert stable3 == 80.0

@pytest.mark.asyncio
async def test_cascading_correlation():
    """Test cascading risk logic."""
    active_hazards = [{"hazard_type": "FLOOD", "id": "flood-1"}]
    cascades = await correlation_engine.detect_cascades(None, "WILDFIRE", "fire-1", active_hazards, "region-1")
    
    assert len(cascades) == 1
    assert cascades[0].interaction_type == "amplification"
    assert cascades[0].amplification_factor == 1.4

def test_fusion_math():
    """Test fusion aggregation and explainability."""
    hazards = [
        {"hazard_type": "WILDFIRE", "reliability_adjusted_score": 60.0},
        {"hazard_type": "FLOOD", "reliability_adjusted_score": 40.0}
    ]
    fused = fusion_engine.execute_fusion("lin-1", "corr-1", hazards, "region-1", "local")
    
    # Max is 60. Compound penalty = (100 - 60) * 0.2 = 8. Fused = 68.0.
    assert fused.fused_score == 68.0
    assert fused.threat_level == "HIGH"
    assert "WILDFIRE" in fused.explanation.contributing_hazards
    assert "FLOOD" in fused.explanation.contributing_hazards

def test_escalation_triggers():
    """Test escalation level assignments."""
    event = escalation_engine.evaluate(86.0, "CRITICAL", [], "region-1", "fused-1")
    assert event.escalation_level == "emergency"
    
    event_catastrophic = escalation_engine.evaluate(96.0, "CRITICAL", ["c-1", "c-2"], "region-1", "fused-1")
    assert event_catastrophic.escalation_level == "catastrophic"

def test_prioritization_capacity_suppression():
    """Test operational capacity suppression."""
    priority = operational_prioritization_engine.calculate_priority(
        "elevated", 60.0, 500, active_queue_depth=100, available_workers=5
    )
    # Queue is saturated (100 / 50 = 2.0 > 0.8). "elevated" is not critical.
    # Base = 20. Fused = 12. Pop = 0. Total = 32. Suppressed = 16.0.
    assert priority == 16.0

def test_geo_aggregation():
    """Test rolling up local assessments into district."""
    child_assessments = [
        {"fused_score": 80.0},
        {"fused_score": 20.0},
        {"fused_score": 20.0}
    ]
    rollup = geo_aggregation_engine.aggregate_regions(child_assessments, "district", "district-1")
    
    # Max = 80. Avg = 40. Rolled = (80 * 0.7) + (40 * 0.3) = 56 + 12 = 68.0
    assert rollup["fused_score"] == 68.0
    assert rollup["child_count"] == 3
    assert rollup["aggregation_hierarchy"]["level"] == "district"
    assert rollup["aggregation_hierarchy"]["parent_region_id"] == "state-parent-of-district-1"
