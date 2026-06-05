from datetime import datetime, timezone
import uuid

from app.core.geospatial.models import BoundingBox
from app.core.satellite.interfaces import SatelliteProvider
from app.core.satellite.models import SatelliteScene, SatelliteMetadata, SatelliteTimeseries

class MockSentinel1Provider(SatelliteProvider):
    def provider_id(self) -> str:
        return "mock_sentinel_1"
        
    def provider_name(self) -> str:
        return "Mock Sentinel-1 (SAR)"

    async def health_check(self) -> dict:
        return {"status": "healthy"}

    async def fetch_scene(self, scene_id: str) -> SatelliteScene:
        # Generate deterministic mock data
        bbox = BoundingBox(min_lon=10.0, min_lat=10.0, max_lon=11.0, max_lat=11.0)
        return SatelliteScene(
            scene_id=scene_id,
            provider=self.provider_id(),
            captured_at=datetime.now(timezone.utc),
            bbox=bbox,
            cloud_cover=0.0, # SAR penetrates clouds
            resolution_meters=10.0,
            bands=["VV", "VH"],
            geometry="POLYGON((10.0 10.0, 11.0 10.0, 11.0 11.0, 10.0 11.0, 10.0 10.0))",
            metadata={"instrument": "C-SAR"}
        )

    async def fetch_timeseries(self, bbox: BoundingBox, start_time: datetime, end_time: datetime) -> SatelliteTimeseries:
        scene = await self.fetch_scene(f"s1_mock_{uuid.uuid4().hex[:8]}")
        return SatelliteTimeseries(
            provider=self.provider_id(),
            location_wkt="POLYGON((...))",
            start_time=start_time,
            end_time=end_time,
            scenes=[scene]
        )

    async def fetch_metadata(self) -> SatelliteMetadata:
        return SatelliteMetadata(
            provider=self.provider_id(),
            metadata={"type": "SAR", "revisit_days": 6}
        )

class MockSentinel2Provider(SatelliteProvider):
    def provider_id(self) -> str:
        return "mock_sentinel_2"
        
    def provider_name(self) -> str:
        return "Mock Sentinel-2 (Multispectral)"

    async def health_check(self) -> dict:
        return {"status": "healthy"}

    async def fetch_scene(self, scene_id: str) -> SatelliteScene:
        bbox = BoundingBox(min_lon=10.0, min_lat=10.0, max_lon=11.0, max_lat=11.0)
        return SatelliteScene(
            scene_id=scene_id,
            provider=self.provider_id(),
            captured_at=datetime.now(timezone.utc),
            bbox=bbox,
            cloud_cover=15.5,
            resolution_meters=10.0,
            bands=["B02", "B03", "B04", "B08"],
            geometry="POLYGON((10.0 10.0, 11.0 10.0, 11.0 11.0, 10.0 11.0, 10.0 10.0))",
            metadata={"instrument": "MSI"}
        )

    async def fetch_timeseries(self, bbox: BoundingBox, start_time: datetime, end_time: datetime) -> SatelliteTimeseries:
        scene = await self.fetch_scene(f"s2_mock_{uuid.uuid4().hex[:8]}")
        return SatelliteTimeseries(
            provider=self.provider_id(),
            location_wkt="POLYGON((...))",
            start_time=start_time,
            end_time=end_time,
            scenes=[scene]
        )

    async def fetch_metadata(self) -> SatelliteMetadata:
        return SatelliteMetadata(
            provider=self.provider_id(),
            metadata={"type": "Multispectral", "revisit_days": 5}
        )
