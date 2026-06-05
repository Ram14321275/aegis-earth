from typing import Dict, List, Optional
import logging

from app.core.satellite.interfaces import SatelliteProvider

logger = logging.getLogger(__name__)

class SatelliteProviderRegistry:
    """
    Central registry for managing dynamic satellite integrations.
    """
    def __init__(self):
        self._providers: Dict[str, SatelliteProvider] = {}

    def register_provider(self, provider: SatelliteProvider) -> None:
        """Registers a provider into the ecosystem"""
        provider_id = provider.provider_id()
        if provider_id in self._providers:
            logger.warning(f"Overwriting existing satellite provider: {provider_id}")
        self._providers[provider_id] = provider
        logger.info(f"Registered satellite provider: {provider.provider_name()} ({provider_id})")

    def unregister_provider(self, provider_id: str) -> None:
        """Removes a provider from the ecosystem"""
        if provider_id in self._providers:
            del self._providers[provider_id]
            logger.info(f"Unregistered satellite provider: {provider_id}")

    def get_provider(self, provider_id: str) -> Optional[SatelliteProvider]:
        """Retrieves a provider by ID, returns None if not found"""
        return self._providers.get(provider_id)

    def list_providers(self) -> List[SatelliteProvider]:
        """Returns all currently registered providers"""
        return list(self._providers.values())

# Global singleton registry
satellite_registry = SatelliteProviderRegistry()
