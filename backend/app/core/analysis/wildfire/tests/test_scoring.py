import pytest
from app.core.analysis.wildfire.models import WildfireRiskScore
from app.core.analysis.wildfire.scoring import WildfireRiskScorer

def test_risk_scoring_extreme_burn():
    score, severity = WildfireRiskScorer.calculate_risk(
        total_burn_area_km2=150.0,
        high_extreme_burn_area_km2=60.0,
        vegetation_loss_percentage=60.0,
        confidence=0.9,
        days_since_acquisition=1.0
    )
    # 60 + 30 + 10 = 100
    assert score == 100.0
    assert severity == WildfireRiskScore.CRITICAL

def test_risk_scoring_low_burn():
    score, severity = WildfireRiskScorer.calculate_risk(
        total_burn_area_km2=2.0,
        high_extreme_burn_area_km2=0.0,
        vegetation_loss_percentage=10.0,
        confidence=0.9,
        days_since_acquisition=1.0
    )
    # 0 + 0 + 0 = 0
    assert score == 0.0
    assert severity == WildfireRiskScore.LOW

def test_risk_scoring_downgrade_unreliable():
    score, severity = WildfireRiskScorer.calculate_risk(
        total_burn_area_km2=150.0,
        high_extreme_burn_area_km2=60.0,
        vegetation_loss_percentage=60.0,
        confidence=0.2, # Unreliable
        days_since_acquisition=10.0 # Unreliable
    )
    assert score == 80.0 # 100 * 0.8
    assert severity == WildfireRiskScore.HIGH # CRITICAL downgraded to HIGH

def test_risk_scoring_moderate():
    score, severity = WildfireRiskScorer.calculate_risk(
        total_burn_area_km2=25.0,
        high_extreme_burn_area_km2=5.0,
        vegetation_loss_percentage=25.0,
        confidence=0.9,
        days_since_acquisition=2.0
    )
    # 20 (high burn > 1) + 15 (total > 20) + 5 (veg loss > 20) = 40
    assert score == 40.0
    assert severity == WildfireRiskScore.MODERATE
