import pytest
import datetime
from unittest.mock import patch, MagicMock

from app.core.geospatial.models import BoundingBox
from app.core.satellite.models import SatelliteScene
from app.core.processing.models import AnalysisReadyDataset, ProcessingMetadata
from app.core.analysis.flood.models import FloodRiskScore
from app.core.analysis.flood.thresholds import ThresholdEvaluator, NDWI_WATER_THRESHOLD, SAR_WATER_THRESHOLD_DB
from app.core.analysis.flood.water_detection import WaterDetector
from app.core.analysis.flood.change_detection import ChangeDetector
from app.core.analysis.flood.risk_scoring import RiskScorer
from app.core.analysis.flood.geojson import GeoJSONGenerator
from app.core.analysis.flood.health import check_flood_engine_health
from app.core.analysis.flood.validators import FloodAnalysisValidator
from app.core.analysis.flood.service import flood_engine_service

# Mock ARD and Scene
mock_bbox = BoundingBox(min_lon=10.0, min_lat=10.0, max_lon=11.0, max_lat=11.0)
mock_scene = SatelliteScene(
    scene_id="S2_MOCK",
    provider="gee",
    captured_at=datetime.datetime.utcnow(),
    bbox=mock_bbox,
    cloud_cover=10.0,
    resolution_meters=10,
    bands=["B3", "B8"],
    geometry="POLYGON((10 10, 11 10, 11 11, 10 11, 10 10))",
    metadata={}
)

mock_ard_s2 = AnalysisReadyDataset(
    ard_id="ard_123",
    scene_id="S2_MOCK",
    bbox=mock_bbox,
    rasters=[],
    indices=[],
    metadata=ProcessingMetadata(
        provider_id="gee",
        scene_id="S2_MOCK",
        processor_version="1.0.0",
        processing_duration_ms=100.0,
        source_collection="COPERNICUS/S2",
        acquisition_date=datetime.datetime.utcnow(),
        cloud_cover=10.0,
        indices_generated=["NDWI"],
        calibrated=True
    )
)

mock_ard_s1 = AnalysisReadyDataset(
    ard_id="ard_124",
    scene_id="S1_MOCK",
    bbox=mock_bbox,
    rasters=[],
    indices=[],
    metadata=ProcessingMetadata(
        provider_id="gee",
        scene_id="S1_MOCK",
        processor_version="1.0.0",
        processing_duration_ms=100.0,
        source_collection="COPERNICUS/S1",
        acquisition_date=datetime.datetime.utcnow(),
        cloud_cover=0.0,
        indices_generated=[],
        calibrated=True
    )
)


def test_ndwi_thresholding():
    # We just ensure the threshold evaluator doesn't crash on mocked calls
    mock_image = MagicMock()
    mock_image.gt.return_value = "MASKED"
    result = ThresholdEvaluator.get_ndwi_water_mask(mock_image)
    assert result == "MASKED"
    mock_image.gt.assert_called_with(NDWI_WATER_THRESHOLD)


def test_sar_thresholding():
    mock_image = MagicMock()
    mock_band = MagicMock()
    mock_image.select.return_value = mock_band
    mock_band.lt.return_value = "SAR_MASKED"
    result = ThresholdEvaluator.get_sar_water_mask(mock_image)
    assert result == "SAR_MASKED"
    mock_image.select.assert_called_with("VV")
    mock_band.lt.assert_called_with(SAR_WATER_THRESHOLD_DB)


@patch("app.core.analysis.flood.water_detection.ee")
def test_water_detection_optical(mock_ee):
    mock_image = MagicMock()
    mock_ee.Image.return_value = mock_image
    mock_ndwi = MagicMock()
    mock_image.normalizedDifference.return_value = mock_ndwi
    mock_mask = MagicMock()
    mock_ndwi.gt.return_value = mock_mask
    mock_mask.rename.return_value = mock_mask
    
    mask, confidence = WaterDetector.detect_water(mock_ard_s2)
    
    assert mask == mock_mask
    assert confidence == 0.9  # 1.0 - (10.0 / 100)
    mock_image.normalizedDifference.assert_called_with(["B3", "B8"])


@patch("app.core.analysis.flood.water_detection.ee")
def test_water_detection_sar(mock_ee):
    mock_image = MagicMock()
    mock_ee.Image.return_value = mock_image
    mock_band = MagicMock()
    mock_image.select.return_value = mock_band
    mock_mask = MagicMock()
    mock_band.lt.return_value = mock_mask
    mock_mask.rename.return_value = mock_mask
    
    mask, confidence = WaterDetector.detect_water(mock_ard_s1)
    
    assert mask == mock_mask
    assert confidence == 0.95
    mock_image.select.assert_called_with("VV")


@patch("app.core.analysis.flood.change_detection.ee")
def test_change_detection(mock_ee):
    mock_current_mask = MagicMock()
    mock_baseline_mask = MagicMock()
    mock_bbox_geom = MagicMock()

    mock_ee.Image.pixelArea.return_value.divide.return_value = MagicMock()

    # We mock the entire reduceRegion chain... a bit tedious, so we patch the methods
    mock_current_mask.multiply.return_value.reduceRegion.return_value.getNumber.return_value.getInfo.return_value = 100.0
    mock_baseline_mask.multiply.return_value.reduceRegion.return_value.getNumber.return_value.getInfo.return_value = 50.0
    
    mock_new_mask = MagicMock()
    mock_current_mask.And.return_value = mock_new_mask
    mock_new_mask.multiply.return_value.reduceRegion.return_value.getNumber.return_value.getInfo.return_value = 50.0

    deltas = ChangeDetector.calculate_inundation(mock_current_mask, mock_baseline_mask, mock_bbox_geom)
    
    assert deltas["current_water_area_km2"] == 100.0
    assert deltas["baseline_water_area_km2"] == 50.0
    assert deltas["newly_inundated_area_km2"] == 50.0
    assert deltas["percentage_increase"] == 100.0
    assert deltas["flood_growth_factor"] == 2.0


def test_risk_scoring():
    # Critical risk
    assert RiskScorer.calculate_risk(51.0, 10.0, 0.9, 10.0, 2.0) == FloodRiskScore.CRITICAL
    assert RiskScorer.calculate_risk(10.0, 150.0, 0.9, 10.0, 2.0) == FloodRiskScore.CRITICAL
    
    # High risk
    assert RiskScorer.calculate_risk(15.0, 10.0, 0.9, 10.0, 2.0) == FloodRiskScore.HIGH
    
    # Moderate risk
    assert RiskScorer.calculate_risk(2.0, 10.0, 0.9, 10.0, 2.0) == FloodRiskScore.MODERATE
    
    # Low risk
    assert RiskScorer.calculate_risk(0.5, 2.0, 0.9, 10.0, 2.0) == FloodRiskScore.LOW
    
    # Unreliable downgrade (Critical -> High)
    assert RiskScorer.calculate_risk(51.0, 10.0, 0.4, 80.0, 10.0) == FloodRiskScore.HIGH


def test_geojson_generation():
    polygons = GeoJSONGenerator.extract_polygons(None, True, mock_bbox)
    assert len(polygons) == 1
    poly = polygons[0]
    assert poly.is_new_inundation is True
    assert poly.geometry_geojson["type"] == "Polygon"


def test_validators():
    # Valid ARD
    FloodAnalysisValidator.validate_ard(mock_ard_s2)
    
    # Invalid optical
    invalid_optical = mock_ard_s2.model_copy(deep=True)
    invalid_optical.metadata.indices_generated = []
    with pytest.raises(ValueError):
        FloodAnalysisValidator.validate_ard(invalid_optical)
        
    # Invalid cloud cover
    cloudy_ard = mock_ard_s2.model_copy(deep=True)
    cloudy_ard.metadata.cloud_cover = 90.0
    with pytest.raises(ValueError):
        FloodAnalysisValidator.validate_ard(cloudy_ard)


def test_health_check():
    health = check_flood_engine_health()
    assert health["status"] == "healthy"
    assert health["ready"] is True


@pytest.mark.anyio
@patch("app.core.analysis.flood.service.baseline_retrieval_service.get_baseline_ard")
@patch("app.core.analysis.flood.service.GEEClient.execute")
async def test_flood_service_orchestration(mock_execute, mock_get_baseline):
    mock_get_baseline.return_value = mock_ard_s2  # Mock baseline
    
    # Mock the GEE execute return value
    mock_execute.return_value = {
        "baseline_water_area_km2": 50.0,
        "current_water_area_km2": 100.0,
        "newly_inundated_area_km2": 50.0,
        "percentage_increase": 100.0,
        "flood_growth_factor": 2.0
    }
    
    with patch("app.core.analysis.flood.water_detection.ee.Image"):
        assessment = await flood_engine_service.analyze(mock_scene, mock_ard_s2, location_id="loc_123")
        
    assert assessment.flooded_area_km2 == 50.0
    assert assessment.severity == FloodRiskScore.HIGH
    assert assessment.metrics.percentage_increase == 100.0
    assert len(assessment.polygons) == 1
    assert assessment.location_id == "loc_123"
