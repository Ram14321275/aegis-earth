import pytest
from app.core.analysis.wildfire.geojson import GeoJSONGenerator
from app.core.geospatial.models import BoundingBox
from app.core.analysis.wildfire.models import BurnSeverityLevel

def test_extract_polygons_valid_geojson():
    bbox = BoundingBox(min_lat=10.0, min_lon=20.0, max_lat=11.0, max_lon=21.0)
    polygons = GeoJSONGenerator.extract_polygons(None, bbox, BurnSeverityLevel.HIGH)
    
    assert len(polygons) == 1
    poly = polygons[0]
    
    assert poly.severity_level == BurnSeverityLevel.HIGH
    assert poly.geometry_geojson["type"] == "Polygon"
    assert len(poly.geometry_geojson["coordinates"]) == 1
    assert len(poly.geometry_geojson["coordinates"][0]) == 5
