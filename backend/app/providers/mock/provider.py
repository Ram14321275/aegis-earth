from typing import Optional

from app.core.logging import get_logger
from app.providers.base import ProviderInterface
from app.providers.contracts import (
    HealthResponse,
    HealthStatus,
    ImageryResponse,
    MetadataResponse,
    ProviderCapabilities,
)

logger = get_logger(__name__)


class MockProvider(ProviderInterface):
    @property
    def name(self) -> str:
        return "Mock Provider"

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
        logger.info(
            "Fetching mock imagery",
            extra={
                "provider": self.name,
                "operation": "get_imagery",
                "lat": lat,
                "lon": lon,
            },
        )
        return ImageryResponse(
            provider_name=self.name,
            provider_version=self.version,
            imagery_data=b"mock_imagery_byte_data",
            format="png",
        )

    async def get_metadata(
        self, lat: float, lon: float, timeout: Optional[float] = None
    ) -> MetadataResponse:
        logger.info(
            "Fetching mock metadata",
            extra={
                "provider": self.name,
                "operation": "get_metadata",
                "lat": lat,
                "lon": lon,
            },
        )
        return MetadataResponse(
            provider_name=self.name,
            provider_version=self.version,
            metadata={"mock_key": "mock_value", "lat": lat, "lon": lon},
        )

    async def health_check(self, timeout: Optional[float] = None) -> HealthResponse:
        logger.info(
            "Running mock health check",
            extra={"provider": self.name, "operation": "health_check"},
        )
        return HealthResponse(
            provider_name=self.name,
            provider_version=self.version,
            status=HealthStatus.HEALTHY,
            details={"latency": "10ms"},
        )
