from app.providers.base import ProviderInterface
from app.providers.contracts import ProviderConfig, ProviderType
from app.providers.gee.provider import GEEProvider
from app.providers.mock.provider import MockProvider
from app.providers.sentinel.provider import SentinelProvider


class ProviderManager:
    @staticmethod
    def get_provider(config: ProviderConfig) -> ProviderInterface:
        if config.provider_type == ProviderType.MOCK:
            return MockProvider(config)
        elif config.provider_type == ProviderType.GEE:
            return GEEProvider(config)
        elif config.provider_type == ProviderType.SENTINEL:
            return SentinelProvider(config)

        raise ValueError(f"Unknown provider type: {config.provider_type}")
