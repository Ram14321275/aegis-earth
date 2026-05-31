from typing import Optional

from app.providers.base import ProviderInterface
from app.providers.contracts import (
    HealthResponse,
    ImageryResponse,
    MetadataResponse,
    ProviderCapabilities,
)


class SentinelProvider(ProviderInterface):
    @property
    def name(self) -> str:
        return "Copernicus Sentinel"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def capabilities(self) -> ProviderCapabilities:
        return ProviderCapabilities(
            supports_imagery=True,
            supports_metadata=True,
            supports_health_checks=True,
        )

    async def get_imagery(
        self, lat: float, lon: float, timeout: Optional[float] = None
    ) -> ImageryResponse:
        raise NotImplementedError("Sentinel integration pending")

    async def get_metadata(
        self, lat: float, lon: float, timeout: Optional[float] = None
    ) -> MetadataResponse:
        raise NotImplementedError("Sentinel integration pending")

    async def health_check(self, timeout: Optional[float] = None) -> HealthResponse:
        raise NotImplementedError("Sentinel integration pending")
