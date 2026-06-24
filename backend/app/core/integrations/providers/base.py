from abc import ABC, abstractmethod
from typing import Any, Dict, List
from pydantic import BaseModel

class ProviderCapabilityMatrix(BaseModel):
    supported_formats: List[str]
    max_batch_size: int
    supports_streaming: bool
    requires_auth: bool

class ProviderInterface(ABC):
    """Abstract base class that all external providers must implement."""

    @property
    @abstractmethod
    def provider_id(self) -> str:
        pass

    @property
    @abstractmethod
    def provider_type(self) -> str:
        pass
        
    @property
    @abstractmethod
    def capabilities(self) -> ProviderCapabilityMatrix:
        pass

    @abstractmethod
    async def fetch_data(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fetch data from the provider."""
        pass

    @abstractmethod
    async def check_health(self) -> bool:
        """Check the health of the provider connection."""
        pass
        
    @abstractmethod
    async def normalize_payload(self, raw_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Convert raw provider payload into a deterministic intermediate representation."""
        pass
