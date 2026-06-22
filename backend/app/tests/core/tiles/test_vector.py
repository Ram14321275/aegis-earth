import pytest
from app.core.tiles.optimization.geometry import geometry_optimizer

def test_calculate_zoom_tolerance():
    # Global view, heavy simplification
    t1 = geometry_optimizer.calculate_zoom_tolerance(4)
    assert t1 == 0.1
    
    # Moderate
    t2 = geometry_optimizer.calculate_zoom_tolerance(8)
    assert t2 == 0.05
    
    # Close up, no simplification
    t3 = geometry_optimizer.calculate_zoom_tolerance(14)
    assert t3 == 0.0

def test_tile_to_bbox():
    # Tile 0,0,0 is the whole world
    bbox = geometry_optimizer.tile_to_bbox(0, 0, 0)
    assert bbox[0] == -180.0
    assert bbox[2] == 180.0
    # Latitude limit for web mercator is ~85.0511
    assert bbox[1] < -85.0
    assert bbox[3] > 85.0
