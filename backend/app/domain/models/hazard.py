from enum import Enum
from typing import List

from pydantic import BaseModel

from app.providers.contracts import ProviderType
from app.schemas.intelligence import SeverityEnum


class HazardType(str, Enum):
    FLOOD = "flood"
    WILDFIRE = "wildfire"
    VEGETATION_LOSS = "vegetation_loss"
    URBAN_EXPANSION = "urban_expansion"
    UNKNOWN = "unknown"


class HazardDefinition(BaseModel):
    hazard_type: HazardType
    display_name: str
    description: str
    severity_levels: List[SeverityEnum]
    supported_providers: List[ProviderType]
