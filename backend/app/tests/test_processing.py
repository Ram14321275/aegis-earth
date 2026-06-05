import pytest
import datetime
from unittest.mock import patch, MagicMock

from app.core.geospatial.models import BoundingBox
from app.core.satellite.models import SatelliteScene
from app.core.processing.pipeline import SentinelProcessingPipeline, sentinel_processing_pipeline

@pytest.fixture
def mock_s1_scene():
    return SatelliteScene(
        scene_id="COPERNICUS/S1_GRD/20210101T000000_10_10",
        provider="mock_sentinel_1",
        captured_at=datetime.datetime.utcnow(),
        bbox=BoundingBox(min_lon=10, min_lat=10, max_lon=11, max_lat=11),
        cloud_cover=0.0,
        resolution_meters=10.0,
        bands=["VV", "VH"],
        geometry="POLYGON((10 10, 11 10, 11 11, 10 11, 10 10))",
        metadata={}
    )

@pytest.fixture
def mock_s2_scene():
    return SatelliteScene(
        scene_id="COPERNICUS/S2_SR/20210101T000000_10_10",
        provider="mock_sentinel_2",
        captured_at=datetime.datetime.utcnow(),
        bbox=BoundingBox(min_lon=10, min_lat=10, max_lon=11, max_lat=11),
        cloud_cover=10.0,
        resolution_meters=10.0,
        bands=["B2", "B3", "B4", "B8", "B12"],
        geometry="POLYGON((10 10, 11 10, 11 11, 10 11, 10 10))",
        metadata={}
    )

def test_sentinel_type_detection(mock_s1_scene, mock_s2_scene):
    assert sentinel_processing_pipeline._detect_type(mock_s1_scene) == "SENTINEL-1"
    assert sentinel_processing_pipeline._detect_type(mock_s2_scene) == "SENTINEL-2"
    
    with pytest.raises(ValueError):
        sentinel_processing_pipeline._detect_type(
            SatelliteScene(
                scene_id="UNKNOWN", provider="unknown",
                captured_at=datetime.datetime.utcnow(),
                bbox=BoundingBox(min_lon=0, min_lat=0, max_lon=1, max_lat=1),
                cloud_cover=0.0, resolution_meters=10.0,
                bands=[], geometry="POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))", metadata={}
            )
        )

@pytest.mark.anyio
@patch("app.core.processing.sentinel1.service.GEEClient.execute")
async def test_s1_processing_pipeline(mock_execute, mock_s1_scene):
    # Mock the GEE Client to just return a dummy info dict
    mock_execute.return_value = {"bands": [{"id": "VV"}, {"id": "VH"}]}
    
    result = await sentinel_processing_pipeline.process_scene(mock_s1_scene)
    
    assert result.success is True
    ard = result.ard
    assert ard.metadata.source_collection == "COPERNICUS/S1_GRD"
    assert ard.metadata.terrain_corrected is True
    assert ard.metadata.calibrated is True
    assert "LEE" in ard.metadata.filters_applied
    
    assert len(ard.rasters) == 2
    assert ard.rasters[0].band_name == "VV"
    assert ard.rasters[1].band_name == "VH"

@pytest.mark.anyio
@patch("app.core.processing.sentinel2.service.GEEClient.execute")
async def test_s2_processing_pipeline(mock_execute, mock_s2_scene):
    # Mock the GEE Client
    mock_execute.return_value = {"bands": [{"id": "B4"}, {"id": "B8"}]}
    
    result = await sentinel_processing_pipeline.process_scene(mock_s2_scene)
    
    assert result.success is True
    ard = result.ard
    assert ard.metadata.source_collection == "COPERNICUS/S2_SR_HARMONIZED"
    assert "CLOUD_MASK" in ard.metadata.filters_applied
    assert "SHADOW_REMOVAL" in ard.metadata.filters_applied
    
    assert "NDVI" in ard.metadata.indices_generated
    assert "NDWI" in ard.metadata.indices_generated
    assert "NBR" in ard.metadata.indices_generated
    
    # Check indices are present structurally
    assert len(ard.indices) == 3
    index_names = [idx.name for idx in ard.indices]
    assert "NDVI" in index_names
    assert "NDWI" in index_names
    assert "NBR" in index_names

@pytest.mark.anyio
@patch("app.core.processing.pipeline.processing_cache.get_ard")
@patch("app.core.processing.pipeline.processing_cache.set_ard")
@patch("app.core.processing.sentinel1.service.GEEClient.execute")
async def test_processing_cache_integration(mock_execute, mock_set, mock_get, mock_s1_scene):
    # First request: Cache Miss
    mock_get.return_value = None
    mock_execute.return_value = {}
    
    result1 = await sentinel_processing_pipeline.process_scene(mock_s1_scene)
    assert result1.success is True
    assert mock_execute.call_count == 1
    assert mock_set.call_count == 1
    
    # Second request: Cache Hit
    mock_get.return_value = result1.ard
    
    result2 = await sentinel_processing_pipeline.process_scene(mock_s1_scene)
    assert result2.success is True
    assert mock_execute.call_count == 1 # Did not increase!
    assert mock_set.call_count == 1 # Did not increase!
