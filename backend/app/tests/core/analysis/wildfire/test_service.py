import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from app.core.analysis.wildfire.service import wildfire_engine_service

@pytest.mark.anyio
@patch("app.core.analysis.wildfire.service.baseline_retrieval_service")
@patch("app.core.analysis.wildfire.service.GEEClient")
async def test_wildfire_service_analyze(mock_gee, mock_baseline):
    mock_scene = MagicMock()
    mock_scene.bbox.min_lon = 0
    mock_scene.bbox.min_lat = 0
    mock_scene.bbox.max_lon = 1
    mock_scene.bbox.max_lat = 1
    
    mock_ard = MagicMock()
    mock_ard.metadata.cloud_cover = 10.0
    mock_ard.metadata.indices_generated = ["NDVI", "NBR"]
    
    mock_baseline.get_baseline_ard = AsyncMock(return_value=None)
    
    mock_gee.execute = AsyncMock(return_value={
        "total_burn_area_km2": 50.0,
        "high_extreme_burn_area_km2": 20.0,
        "vegetation_impact": {
            "baseline_ndvi": 0.6,
            "current_ndvi": 0.2,
            "vegetation_loss_percentage": 66.6,
            "affected_area_km2": 50.0
        }
    })
    
    result = await wildfire_engine_service.analyze(mock_scene, mock_ard)
    
    assert result.assessment.burned_area_km2 == 50.0
    assert result.assessment.metrics.total_burn_area_km2 == 50.0
    # Baseline was none, so confidence is low (0.1) and risk is downgraded
    # total=50 (15), high=20 (25), veg=66.6 (20) -> base score 60.
    # Unreliable downgrade (confidence < 0.5): 60 * 0.8 = 48.0
    assert result.assessment.severity.value == "MODERATE"
