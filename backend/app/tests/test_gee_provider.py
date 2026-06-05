import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import patch, MagicMock, AsyncMock

from app.core.geospatial.models import BoundingBox
from app.core.satellite.providers.gee_provider import GoogleEarthEngineProvider
from app.integrations.gee.circuit_breaker import gee_circuit_breaker, CircuitState

@pytest.fixture
def gee_provider():
    return GoogleEarthEngineProvider()

@pytest.fixture
def mock_bbox():
    return BoundingBox(min_lon=10.0, min_lat=10.0, max_lon=11.0, max_lat=11.0)

def test_gee_provider_registration(gee_provider):
    assert gee_provider.provider_id() == "google_earth_engine"
    assert gee_provider.provider_name() == "Google Earth Engine"

@pytest.mark.anyio
@patch("app.integrations.gee.client.GEEAuthenticator.is_authenticated")
@patch("app.integrations.gee.health.GEEClient.execute")
async def test_health_check_healthy(mock_execute, mock_auth, gee_provider):
    mock_auth.return_value = True
    mock_execute.return_value = 1
    
    health = await gee_provider.health_check()
    assert health["status"] == "healthy"
    assert health["authenticated"] is True
    assert health["collections_available"] is True

@pytest.mark.anyio
@patch("app.integrations.gee.client.GEEAuthenticator.is_authenticated")
@patch("app.integrations.gee.health.GEEClient.execute")
async def test_health_check_unhealthy(mock_execute, mock_auth, gee_provider):
    mock_auth.return_value = False
    mock_execute.side_effect = Exception("Connection refused")
    
    health = await gee_provider.health_check()
    assert health["status"] == "unhealthy"
    assert health["authenticated"] is False

@pytest.mark.anyio
@patch("app.integrations.gee.client.GEEAuthenticator.is_authenticated")
@patch("app.integrations.gee.client.GEEAuthenticator.authenticate_and_initialize")
async def test_auth_initialization(mock_init, mock_auth, gee_provider):
    mock_auth.return_value = False
    mock_init.return_value = False
    
    # Reset circuit breaker
    gee_circuit_breaker.record_success()
    
    with pytest.raises(RuntimeError, match="GEE is not authenticated"):
        await gee_provider.fetch_scene("dummy")

@pytest.mark.anyio
@patch("app.integrations.gee.client.GEEAuthenticator.is_authenticated", return_value=True)
@patch("app.core.satellite.providers.gee_provider.ee.Image")
@patch("app.core.satellite.providers.gee_provider.ee.Geometry")
async def test_fetch_scene(mock_geom, mock_image_cls, mock_auth, gee_provider):
    # Setup GEE mocks
    mock_image = MagicMock()
    mock_image.getInfo.return_value = {
        "properties": {
            "system:time_start": 1609459200000, # Jan 1, 2021
            "CLOUDY_PIXEL_PERCENTAGE": 12.5
        },
        "bands": [{"id": "B2"}, {"id": "B3"}, {"id": "B4"}]
    }
    mock_image_cls.return_value = mock_image
    
    mock_bounds = MagicMock()
    mock_bounds.bounds().getInfo.return_value = {
        "coordinates": [[[10, 10], [11, 10], [11, 11], [10, 11], [10, 10]]]
    }
    mock_geom.return_value = mock_bounds
    
    # Reset circuit breaker
    gee_circuit_breaker.record_success()
    
    scene = await gee_provider.fetch_scene("COPERNICUS/S2_SR/20210101T100000_10_10")
    
    assert scene.scene_id == "COPERNICUS/S2_SR/20210101T100000_10_10"
    assert scene.cloud_cover == 12.5
    assert len(scene.bands) == 3
    assert scene.bbox.min_lon == 10
    assert scene.bbox.max_lat == 11

@pytest.mark.anyio
@patch("app.integrations.gee.client.GEEAuthenticator.is_authenticated", return_value=True)
@patch("app.integrations.gee.client.asyncio.to_thread")
async def test_retry_and_circuit_breaker(mock_to_thread, mock_auth, gee_provider):
    mock_to_thread.side_effect = Exception("Transient GEE Error")
    gee_circuit_breaker.failure_threshold = 2
    gee_circuit_breaker.record_success()
    
    # The provider method @retry should attempt 3 times (thus failing the circuit breaker)
    with pytest.raises(Exception):
        await gee_provider.fetch_scene("dummy")
        
    assert gee_circuit_breaker.state == CircuitState.OPEN
    
    # Next call should be denied immediately by circuit breaker
    with pytest.raises(RuntimeError, match="GEE Circuit Breaker is OPEN"):
        await gee_provider.fetch_scene("dummy")
