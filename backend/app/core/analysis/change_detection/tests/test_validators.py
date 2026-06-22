import pytest
from app.core.analysis.change_detection.models import ChangeWindow
from app.core.analysis.change_detection.validators import TemporalValidator
from app.core.geospatial.models import BoundingBox

def test_validate_window():
    assert TemporalValidator.validate_window(ChangeWindow.DAYS_7) == 7
    assert TemporalValidator.validate_window(ChangeWindow.DAYS_30) == 30
    assert TemporalValidator.validate_window(ChangeWindow.YEAR_1) == 365
    assert TemporalValidator.validate_window(ChangeWindow.CUSTOM, custom_days=100) == 100

def test_validate_window_exceeds_limit():
    with pytest.raises(ValueError):
        TemporalValidator.validate_window(ChangeWindow.CUSTOM, custom_days=6*365)

def test_validate_spatial_bounds():
    bbox = BoundingBox(min_lat=0, max_lat=1, min_lon=0, max_lon=1)
    # Should not raise
    TemporalValidator.validate_spatial_bounds(bbox, area_km2=4000.0)
    
    # Should raise
    with pytest.raises(ValueError):
        TemporalValidator.validate_spatial_bounds(bbox, area_km2=6000.0)
