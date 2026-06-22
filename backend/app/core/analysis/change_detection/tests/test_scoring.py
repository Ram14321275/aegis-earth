import pytest
from app.core.analysis.change_detection.models import (
    ChangeMetrics, SpectralDelta, ChangeDirection, EnvironmentalRiskCategory
)
from app.core.analysis.change_detection.scoring import EnvironmentalChangeScorer

def create_mock_metrics(
    ndvi_dir=ChangeDirection.STABLE, ndvi_area=0.0,
    ndwi_dir=ChangeDirection.STABLE, ndwi_area=0.0,
    nbr_dir=ChangeDirection.STABLE, nbr_area=0.0,
    ndbi_dir=ChangeDirection.STABLE, ndbi_area=0.0
):
    return ChangeMetrics(
        ndvi_delta=SpectralDelta(mean_delta=0, max_loss=0, max_gain=0, direction=ndvi_dir, significant_change_area_km2=ndvi_area),
        ndwi_delta=SpectralDelta(mean_delta=0, max_loss=0, max_gain=0, direction=ndwi_dir, significant_change_area_km2=ndwi_area),
        nbr_delta=SpectralDelta(mean_delta=0, max_loss=0, max_gain=0, direction=nbr_dir, significant_change_area_km2=nbr_area),
        ndbi_delta=SpectralDelta(mean_delta=0, max_loss=0, max_gain=0, direction=ndbi_dir, significant_change_area_km2=ndbi_area),
        cloud_cover_variance=0.0
    )

def test_environmental_scoring_stable():
    metrics = create_mock_metrics()
    score, category, alertable = EnvironmentalChangeScorer.calculate_risk(metrics, confidence=1.0)
    assert score == 0.0
    assert category == EnvironmentalRiskCategory.STABLE
    assert not alertable

def test_environmental_scoring_critical_change():
    # Massive vegetation loss and burn
    metrics = create_mock_metrics(
        ndvi_dir=ChangeDirection.LOSS, ndvi_area=30.0, # 30 * 2 = 60 (capped at 50)
        nbr_dir=ChangeDirection.LOSS, nbr_area=20.0    # 20 * 3 = 60 (capped at 40)
    )
    score, category, alertable = EnvironmentalChangeScorer.calculate_risk(metrics, confidence=1.0)
    assert score == 90.0
    assert category == EnvironmentalRiskCategory.CRITICAL_CHANGE
    assert alertable

def test_environmental_scoring_downgrade():
    metrics = create_mock_metrics(
        ndvi_dir=ChangeDirection.LOSS, ndvi_area=30.0,
        nbr_dir=ChangeDirection.LOSS, nbr_area=20.0
    )
    # With confidence 0.5, score drops from 90 to 45
    score, category, alertable = EnvironmentalChangeScorer.calculate_risk(metrics, confidence=0.5)
    assert score == 45.0
    assert category == EnvironmentalRiskCategory.MODERATE_CHANGE
    assert not alertable
