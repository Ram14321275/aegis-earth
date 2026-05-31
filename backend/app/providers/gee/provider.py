from typing import Optional

from app.providers.base import ProviderInterface
from app.providers.contracts import (
    HealthResponse,
    ImageryResponse,
    MetadataResponse,
    ProviderCapabilities,
)


class GEEProvider(ProviderInterface):
    @property
    def name(self) -> str:
        return "Google Earth Engine"

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
        raise NotImplementedError("GEE integration pending")

    async def get_metadata(
        self, lat: float, lon: float, timeout: Optional[float] = None
    ) -> MetadataResponse:
        raise NotImplementedError("GEE integration pending")

    async def health_check(self, timeout: Optional[float] = None) -> HealthResponse:
        raise NotImplementedError("GEE integration pending")
