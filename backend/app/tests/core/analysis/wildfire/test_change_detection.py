import pytest
from unittest.mock import patch, MagicMock
from app.core.analysis.wildfire.change_detection import WildfireChangeDetector

@patch("app.core.analysis.wildfire.change_detection.ee")
def test_calculate_burn_metrics(mock_ee):
    # Mocking GEE is tricky, we just verify it calls the right methods
    mock_image = MagicMock()
    mock_ee.Image.return_value = mock_image
    
    mock_current_ard = MagicMock()
    mock_current_ard.scene_id = "current_scene"
    mock_baseline_ard = MagicMock()
    mock_baseline_ard.scene_id = "baseline_scene"
    
    # Mock evaluate return
    mock_dnbr = MagicMock()
    mock_image.normalizedDifference.return_value = mock_dnbr
    mock_dnbr.subtract.return_value = mock_dnbr
    mock_dnbr.gt.return_value = mock_dnbr
    
    mock_reduce = MagicMock()
    mock_dnbr.multiply.return_value.reduceRegion.return_value = mock_reduce
    # Make getInfo return a float instead of a MagicMock when called via getNumber
    mock_reduce.getNumber.return_value.getInfo.return_value = 10.5
    
    # Also need to mock reduceRegion for baseline_ndvi and current_ndvi
    mock_baseline_ndvi = MagicMock()
    mock_current_ndvi = MagicMock()
    mock_image.normalizedDifference.side_effect = [mock_dnbr, mock_dnbr, mock_current_ndvi, mock_baseline_ndvi]
    mock_baseline_ndvi.reduceRegion.return_value.getNumber.return_value.getInfo.return_value = 0.8
    mock_current_ndvi.reduceRegion.return_value.getNumber.return_value.getInfo.return_value = 0.4
    
    metrics = WildfireChangeDetector.calculate_burn_metrics(mock_current_ard, mock_baseline_ard, MagicMock())
    
    assert metrics["total_burn_area_km2"] == 10.5
    assert metrics["high_extreme_burn_area_km2"] == 10.5
    assert metrics["vegetation_impact"]["baseline_ndvi"] == 0.8
    assert metrics["vegetation_impact"]["current_ndvi"] == 0.4
    assert metrics["vegetation_impact"]["vegetation_loss_percentage"] == 50.0
