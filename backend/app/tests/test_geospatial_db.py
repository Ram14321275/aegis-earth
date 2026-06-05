import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from app.core.geospatial.models import Point, BoundingBox, RadiusSearch, PolygonArea
from app.core.geospatial.validators import validate_bounding_box, validate_polygon_closed
from app.core.geospatial.service import (
    get_distance_between_points,
    find_locations_within_radius,
    find_locations_in_bbox,
    find_locations_in_polygon,
    find_locations_intersecting_hazard
)
from app.core.exceptions import ValidationError
from app.observability.metrics import metrics_store
from app.db.models.location import Location

@pytest.fixture
def mock_session():
    return AsyncMock()

@pytest.mark.anyio
async def test_distance_between_points(mock_session):
    # Setup mock
    mock_result = MagicMock()
    mock_result.scalar.return_value = 1500.5
    mock_session.execute.return_value = mock_result
    
    p1 = Point(lat=10.0, lon=20.0)
    p2 = Point(lat=10.1, lon=20.1)
    
    distance = await get_distance_between_points(mock_session, p1, p2)
    
    assert distance == 1500.5
    # Verify spatial metrics recorded
    metrics = metrics_store.get_metrics()
    assert metrics.spatial.spatial_queries_total >= 1

@pytest.mark.anyio
async def test_find_locations_within_radius(mock_session):
    mock_result = MagicMock()
    
    # Mocking result.scalars().all()
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = [Location(city="Test City")]
    mock_result.scalars.return_value = mock_scalars
    
    mock_session.execute.return_value = mock_result
    
    search = RadiusSearch(center=Point(lat=10.0, lon=20.0), radius_meters=5000.0)
    
    locations = await find_locations_within_radius(mock_session, search)
    assert len(locations) == 1
    assert locations[0].city == "Test City"

@pytest.mark.anyio
async def test_find_locations_in_bbox_validation():
    # Invalid bbox: min > max
    bbox = BoundingBox(min_lon=50.0, min_lat=50.0, max_lon=10.0, max_lat=10.0)
    
    with pytest.raises(ValidationError):
        validate_bounding_box(bbox)

@pytest.mark.anyio
async def test_find_locations_in_bbox(mock_session):
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = [Location(city="BBox City")]
    mock_result.scalars.return_value = mock_scalars
    mock_session.execute.return_value = mock_result
    
    bbox = BoundingBox(min_lon=10.0, min_lat=10.0, max_lon=20.0, max_lat=20.0)
    locations = await find_locations_in_bbox(mock_session, bbox)
    assert len(locations) == 1
    assert locations[0].city == "BBox City"

@pytest.mark.anyio
async def test_find_locations_in_polygon_validation():
    # Polygon that does not close
    poly = PolygonArea(coordinates=[(10.0, 10.0), (20.0, 10.0), (20.0, 20.0)])
    
    with pytest.raises(ValidationError):
        validate_polygon_closed(poly)

@pytest.mark.anyio
async def test_find_locations_in_polygon(mock_session):
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = [Location(city="Polygon City")]
    mock_result.scalars.return_value = mock_scalars
    mock_session.execute.return_value = mock_result
    
    poly = PolygonArea(coordinates=[(10.0, 10.0), (20.0, 10.0), (20.0, 20.0), (10.0, 10.0)])
    locations = await find_locations_in_polygon(mock_session, poly)
    assert len(locations) == 1

@pytest.mark.anyio
async def test_health_check_postgis():
    from app.core.geospatial.health import check_postgis_health
    
    # Mock AsyncSessionLocal and session.execute
    mock_session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar.return_value = "3.3.2 USE_GEOS=1 USE_PROJ=1 USE_STATS=1"
    mock_session.execute.return_value = mock_result

    # Mock AsyncSessionLocal as context manager
    mock_session_maker = MagicMock()
    mock_session_maker.return_value.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session_maker.return_value.__aexit__ = AsyncMock(return_value=None)

    with patch("app.core.geospatial.health.AsyncSessionLocal", new=mock_session_maker):
        health = await check_postgis_health()
        assert health["status"] == "healthy"
        assert "3.3.2" in health["version"]
        assert health["spatial_indexes"] is True
