import pytest
from app.core.analysis.wildfire.scoring import WildfireRiskScorer
from app.core.analysis.wildfire.models import WildfireRiskScore

def test_extreme_burn_critical_risk():
    score, severity = WildfireRiskScorer.calculate_risk(
        total_burn_area_km2=200.0,
        high_extreme_burn_area_km2=60.0,
        vegetation_loss_percentage=60.0,
        confidence=0.9,
        days_since_acquisition=2.0
    )
    assert severity == WildfireRiskScore.CRITICAL
    assert score == 100.0

def test_low_burn_low_risk():
    score, severity = WildfireRiskScorer.calculate_risk(
        total_burn_area_km2=2.0,
        high_extreme_burn_area_km2=0.0,
        vegetation_loss_percentage=5.0,
        confidence=0.9,
        days_since_acquisition=1.0
    )
    assert severity == WildfireRiskScore.LOW
    assert score == 0.0

def test_unreliable_downgrade():
    score, severity = WildfireRiskScorer.calculate_risk(
        total_burn_area_km2=200.0,
        high_extreme_burn_area_km2=60.0,
        vegetation_loss_percentage=60.0,
        confidence=0.2, # Very low confidence
        days_since_acquisition=2.0
    )
    assert severity == WildfireRiskScore.HIGH
    assert score == 80.0 # 100 * 0.8
