from typing import Protocol, List
from datetime import datetime

from app.core.geospatial.models import BoundingBox
from app.core.satellite.models import SatelliteScene, SatelliteMetadata, SatelliteTimeseries

class SatelliteProvider(Protocol):
    """
    Abstract interface defining the contract for all satellite providers.
    Every integration (Sentinel, Earth Engine, Maxar) must conform to this protocol.
    """
    
    def provider_id(self) -> str:
        """Returns the unique identifier for the provider (e.g. 'sentinel_1')"""
        ...
        
    def provider_name(self) -> str:
        """Returns the human-readable name of the provider"""
        ...

    async def health_check(self) -> dict:
        """
        Validates connection to the provider. 
        Must return a dict with at minimum {'status': 'healthy' | 'unhealthy'}
        """
        ...

    async def fetch_scene(self, scene_id: str) -> SatelliteScene:
        """Fetches a specific satellite scene by its unique ID"""
        ...

    async def fetch_timeseries(self, bbox: BoundingBox, start_time: datetime, end_time: datetime) -> SatelliteTimeseries:
        """Fetches a chronological series of scenes for a specific region"""
        ...

    async def fetch_metadata(self) -> SatelliteMetadata:
        """Fetches generic provider-level capabilities and limits"""
        ...
