import pytest
from app.core.geospatial.models import BoundingBox
from app.core.analysis.change_detection.models import ChangeType, ChangeDirection
from app.core.analysis.change_detection.geojson import ChangeGeoJSONGenerator

def test_geojson_generator():
    bbox = BoundingBox(min_lat=0, max_lat=1, min_lon=0, max_lon=1)
    
    # Area = 0 should return empty list
    polys = ChangeGeoJSONGenerator.extract_polygons(
        bbox, ChangeType.VEGETATION, ChangeDirection.LOSS, "Past 30d", 0.9, ["scene_1"], 0.0
    )
    assert len(polys) == 0
    
    # Area > 0 should return a single bounded polygon
    polys = ChangeGeoJSONGenerator.extract_polygons(
        bbox, ChangeType.VEGETATION, ChangeDirection.LOSS, "Past 30d", 0.9, ["scene_1"], 10.0
    )
    assert len(polys) == 1
    poly = polys[0]
    
    assert poly.area_km2 == 10.0
    assert poly.change_type == ChangeType.VEGETATION
    assert poly.direction == ChangeDirection.LOSS
    assert poly.timeframe == "Past 30d"
    assert poly.confidence == 0.9
    assert poly.source_scene_ids == ["scene_1"]
    assert poly.geometry_geojson["type"] == "Polygon"
