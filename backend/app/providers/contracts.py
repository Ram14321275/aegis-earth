from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel


class ProviderType(str, Enum):
    MOCK = "mock"
    GEE = "gee"
    SENTINEL = "sentinel"


class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"


class ProviderCapabilities(BaseModel):
    supports_imagery: bool
    supports_metadata: bool
    supports_health_checks: bool


class ProviderConfig(BaseModel):
    provider_type: ProviderType = ProviderType.MOCK
    timeout_seconds: float = 30.0
    retry_limit: int = 3


class ImageryResponse(BaseModel):
    provider_name: str
    provider_version: str
    imagery_data: bytes
    format: str


class MetadataResponse(BaseModel):
    provider_name: str
    provider_version: str
    metadata: Dict[str, Any]


class HealthResponse(BaseModel):
    provider_name: str
    provider_version: str
    status: HealthStatus
    details: Optional[Dict[str, Any]] = None
