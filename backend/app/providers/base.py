from abc import ABC, abstractmethod
from typing import Optional

from app.providers.contracts import (
    HealthResponse,
    ImageryResponse,
    MetadataResponse,
    ProviderCapabilities,
    ProviderConfig,
)


class ProviderInterface(ABC):
    def __init__(self, config: ProviderConfig):
        self.config = config

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        pass

    @property
    @abstractmethod
    def capabilities(self) -> ProviderCapabilities:
        pass

    @abstractmethod
    async def get_imagery(
        self, lat: float, lon: float, timeout: Optional[float] = None
    ) -> ImageryResponse:
        pass

    @abstractmethod
    async def get_metadata(
        self, lat: float, lon: float, timeout: Optional[float] = None
    ) -> MetadataResponse:
        pass

    @abstractmethod
    async def health_check(self, timeout: Optional[float] = None) -> HealthResponse:
        pass
