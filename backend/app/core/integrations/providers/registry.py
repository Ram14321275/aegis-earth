from typing import Dict, Optional
from app.core.integrations.providers.base import ProviderInterface
import logging

logger = logging.getLogger(__name__)

class ProviderRegistry:
    def __init__(self):
        self._providers: Dict[str, ProviderInterface] = {}

    def register(self, provider: ProviderInterface) -> None:
        if provider.provider_id in self._providers:
            logger.warning(f"Provider {provider.provider_id} already registered. Overwriting.")
        self._providers[provider.provider_id] = provider
        logger.info(f"Registered provider: {provider.provider_id} of type {provider.provider_type}")

    def get(self, provider_id: str) -> Optional[ProviderInterface]:
        return self._providers.get(provider_id)

    def get_all(self) -> Dict[str, ProviderInterface]:
        return self._providers.copy()

    def get_by_type(self, provider_type: str) -> Dict[str, ProviderInterface]:
        return {k: v for k, v in self._providers.items() if v.provider_type == provider_type}

provider_registry = ProviderRegistry()
