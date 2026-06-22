import pytest
from app.core.analysis.wildfire.models import (
    BurnSeverityLevel, WildfireRiskScore, BurnPolygon, VegetationImpact,
    WildfireMetrics, WildfireAssessment, WildfireAnalysisResult
)

def test_burn_polygon_creation():
    poly = BurnPolygon(
        id="poly-1",
        geometry_geojson={"type": "Polygon", "coordinates": [[[0,0], [1,0], [1,1], [0,1], [0,0]]]},
        area_km2=5.0,
        severity_level=BurnSeverityLevel.MODERATE
    )
    assert poly.area_km2 == 5.0
    assert poly.severity_level == "MODERATE"

def test_wildfire_assessment_creation():
    veg_impact = VegetationImpact(
        baseline_ndvi=0.6,
        current_ndvi=0.3,
        vegetation_loss_percentage=50.0,
        affected_area_km2=10.0
    )
    
    metrics = WildfireMetrics(
        total_burn_area_km2=10.0,
        high_extreme_burn_area_km2=2.0,
        vegetation_impact=veg_impact,
        cloud_cover_percent=0.0
    )
    
    assessment = WildfireAssessment(
        assessment_id="test-1",
        burned_area_km2=10.0,
        confidence=0.9,
        severity=WildfireRiskScore.HIGH,
        metrics=metrics
    )
    
    assert assessment.severity == "HIGH"
    assert assessment.metrics.vegetation_impact.vegetation_loss_percentage == 50.0
