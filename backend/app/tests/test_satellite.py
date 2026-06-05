import pytest
from datetime import datetime, timezone, timedelta
import json
from unittest.mock import AsyncMock, patch

from app.core.satellite.models import SatelliteScene, SatelliteTimeseries
from app.core.geospatial.models import BoundingBox
from app.core.satellite.registry import SatelliteProviderRegistry
from app.core.satellite.providers.mock_providers import MockSentinel1Provider, MockSentinel2Provider
from app.core.satellite.service import satellite_service
from app.core.exceptions import ValidationError

@pytest.fixture
def registry():
    reg = SatelliteProviderRegistry()
    reg.register_provider(MockSentinel1Provider())
    reg.register_provider(MockSentinel2Provider())
    return reg

def test_registry_registration(registry):
    providers = registry.list_providers()
    assert len(providers) == 2
    
    p1 = registry.get_provider("mock_sentinel_1")
    assert p1 is not None
    assert p1.provider_name() == "Mock Sentinel-1 (SAR)"
    
    registry.unregister_provider("mock_sentinel_1")
    assert registry.get_provider("mock_sentinel_1") is None
    assert len(registry.list_providers()) == 1

@pytest.mark.anyio
async def test_mock_provider_fetch_scene():
    provider = MockSentinel2Provider()
    scene = await provider.fetch_scene("test_scene")
    
    assert scene.scene_id == "test_scene"
    assert scene.provider == "mock_sentinel_2"
    assert scene.cloud_cover == 15.5
    assert len(scene.bands) == 4

@pytest.mark.anyio
async def test_mock_provider_fetch_timeseries():
    provider = MockSentinel1Provider()
    bbox = BoundingBox(min_lon=10.0, min_lat=10.0, max_lon=11.0, max_lat=11.0)
    start_time = datetime.now(timezone.utc) - timedelta(days=30)
    end_time = datetime.now(timezone.utc)
    
    timeseries = await provider.fetch_timeseries(bbox, start_time, end_time)
    assert len(timeseries.scenes) == 1
    assert timeseries.scenes[0].provider == "mock_sentinel_1"

@pytest.mark.anyio
async def test_satellite_service_validation():
    bbox = BoundingBox(min_lon=10.0, min_lat=10.0, max_lon=11.0, max_lat=11.0)
    start_time = datetime.now(timezone.utc)
    end_time = datetime.now(timezone.utc) - timedelta(days=1)
    
    # End time before start time
    with pytest.raises(ValidationError):
        await satellite_service.fetch_timeseries("mock_sentinel_1", bbox, start_time, end_time)
        
    start_time_far = datetime.now(timezone.utc) - timedelta(days=400)
    end_time_now = datetime.now(timezone.utc)
    
    # Exceeds 365 days
    with pytest.raises(ValidationError):
        await satellite_service.fetch_timeseries("mock_sentinel_1", bbox, start_time_far, end_time_now)

@pytest.mark.anyio
@patch("app.core.satellite.service.cache_manager")
@patch("app.core.satellite.service.satellite_registry")
async def test_satellite_service_cache_hit(mock_registry, mock_cache):
    # Setup mock registry
    mock_provider = MockSentinel1Provider()
    mock_registry.get_provider.return_value = mock_provider
    
    # Setup mock cache
    scene = await mock_provider.fetch_scene("test_123")
    mock_cache.get = AsyncMock(return_value=scene.model_dump_json())
    mock_cache.set = AsyncMock()
    
    # Fetch
    result = await satellite_service.fetch_scene("mock_sentinel_1", "test_123")
    
    # Verify we hit cache and didn't call set
    mock_cache.get.assert_called_once()
    mock_cache.set.assert_not_called()
    assert result.scene_id == "test_123"

@pytest.mark.anyio
@patch("app.core.satellite.service.cache_manager")
@patch("app.core.satellite.service.satellite_registry")
async def test_satellite_service_cache_miss(mock_registry, mock_cache):
    # Setup mock registry
    mock_provider = MockSentinel1Provider()
    mock_registry.get_provider.return_value = mock_provider
    
    # Cache miss
    mock_cache.get = AsyncMock(return_value=None)
    mock_cache.set = AsyncMock()
    
    # Fetch
    result = await satellite_service.fetch_scene("mock_sentinel_1", "test_123")
    
    # Verify cache get and set were called
    mock_cache.get.assert_called_once()
    mock_cache.set.assert_called_once()
    assert result.scene_id == "test_123"

@pytest.mark.anyio
async def test_satellite_health():
    from app.core.satellite.health import get_satellite_system_health
    from app.core.satellite.registry import satellite_registry
    
    # Ensure providers are registered for the global registry in this test
    if not satellite_registry.get_provider("mock_sentinel_1"):
        satellite_registry.register_provider(MockSentinel1Provider())
    if not satellite_registry.get_provider("mock_sentinel_2"):
        satellite_registry.register_provider(MockSentinel2Provider())
        
    health = await get_satellite_system_health()
    assert health["providers"] >= 2
    assert health["healthy"] >= 2
    assert health["unhealthy"] == 0
