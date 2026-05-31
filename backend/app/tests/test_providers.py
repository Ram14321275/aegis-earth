import pytest

from app.providers.contracts import HealthStatus, ProviderConfig, ProviderType
from app.providers.gee.provider import GEEProvider
from app.providers.manager import ProviderManager
from app.providers.mock.provider import MockProvider
from app.providers.sentinel.provider import SentinelProvider


def test_provider_manager_factory():
    config_mock = ProviderConfig(provider_type=ProviderType.MOCK)
    provider_mock = ProviderManager.get_provider(config_mock)
    assert isinstance(provider_mock, MockProvider)
    assert provider_mock.name == "Mock Provider"

    config_gee = ProviderConfig(provider_type=ProviderType.GEE)
    provider_gee = ProviderManager.get_provider(config_gee)
    assert isinstance(provider_gee, GEEProvider)

    config_sentinel = ProviderConfig(provider_type=ProviderType.SENTINEL)
    provider_sentinel = ProviderManager.get_provider(config_sentinel)
    assert isinstance(provider_sentinel, SentinelProvider)


def test_provider_capabilities():
    config = ProviderConfig(provider_type=ProviderType.MOCK)
    provider = ProviderManager.get_provider(config)
    caps = provider.capabilities
    assert caps.supports_imagery is True
    assert caps.supports_metadata is True
    assert caps.supports_health_checks is True


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_mock_provider_imagery_and_metadata():
    config = ProviderConfig(provider_type=ProviderType.MOCK)
    provider = ProviderManager.get_provider(config)

    imagery = await provider.get_imagery(17.385, 78.486)
    assert imagery.imagery_data == b"mock_imagery_byte_data"
    assert imagery.provider_name == provider.name

    metadata = await provider.get_metadata(17.385, 78.486)
    assert "mock_key" in metadata.metadata
    assert metadata.provider_name == provider.name


@pytest.mark.anyio
async def test_mock_provider_health():
    config = ProviderConfig(provider_type=ProviderType.MOCK)
    provider = ProviderManager.get_provider(config)

    health = await provider.health_check()
    assert health.status == HealthStatus.HEALTHY
    assert health.provider_name == provider.name
    assert health.details is not None
