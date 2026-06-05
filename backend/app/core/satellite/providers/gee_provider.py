from datetime import datetime, timezone
import ee
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from app.core.satellite.interfaces import SatelliteProvider
from app.core.satellite.models import SatelliteScene, SatelliteMetadata, SatelliteTimeseries
from app.core.geospatial.models import BoundingBox
from app.integrations.gee.client import GEEClient
from app.integrations.gee.collections import GEECollection, COLLECTION_BANDS
from app.integrations.gee.filters import create_bbox_geometry, apply_date_filter, apply_bounds_filter
from app.integrations.gee.health import check_gee_health

class GoogleEarthEngineProvider(SatelliteProvider):
    def provider_id(self) -> str:
        return "google_earth_engine"

    def provider_name(self) -> str:
        return "Google Earth Engine"

    async def health_check(self) -> dict:
        return await check_gee_health()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True
    )
    async def fetch_scene(self, scene_id: str) -> SatelliteScene:
        """
        Fetches a specific scene by parsing the GEE Image ID directly.
        """
        def _fetch_image():
            image = ee.Image(scene_id)
            info = image.getInfo()
            
            # GEE returns geometry coordinates, we build a simple WKT polygon for the bounding box
            footprint = ee.Geometry(info.get('properties', {}).get('system:footprint', image.geometry())).bounds().getInfo()
            coords = footprint.get('coordinates', [[[0,0]]])[0]
            
            # Extract bounds
            lons = [c[0] for c in coords]
            lats = [c[1] for c in coords]
            
            bbox = BoundingBox(
                min_lon=min(lons),
                min_lat=min(lats),
                max_lon=max(lons),
                max_lat=max(lats)
            )
            
            wkt = f"POLYGON(({min(lons)} {min(lats)}, {max(lons)} {min(lats)}, {max(lons)} {max(lats)}, {min(lons)} {max(lats)}, {min(lons)} {min(lats)}))"
            
            # Epoch milliseconds to UTC datetime
            timestamp_ms = info.get('properties', {}).get('system:time_start', 0)
            captured_at = datetime.fromtimestamp(timestamp_ms / 1000.0, tz=timezone.utc)
            
            return SatelliteScene(
                scene_id=scene_id,
                provider=self.provider_id(),
                captured_at=captured_at,
                bbox=bbox,
                cloud_cover=info.get('properties', {}).get('CLOUDY_PIXEL_PERCENTAGE', 0.0),
                resolution_meters=10.0, # default Sentinel
                bands=[b['id'] for b in info.get('bands', [])],
                geometry=wkt,
                metadata=info.get('properties', {})
            )

        return await GEEClient.execute(_fetch_image)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True
    )
    async def fetch_timeseries(self, bbox: BoundingBox, start_time: datetime, end_time: datetime) -> SatelliteTimeseries:
        """
        Fetches a timeseries of Sentinel-2 images over a bounding box.
        """
        def _fetch_collection():
            geom = create_bbox_geometry(bbox)
            collection = ee.ImageCollection(GEECollection.SENTINEL_2_OPTICAL)
            collection = apply_date_filter(collection, start_time, end_time)
            collection = apply_bounds_filter(collection, geom)
            
            # Get up to 50 scenes maximum to prevent OOM
            info = collection.limit(50).getInfo()
            
            scenes = []
            for img in info.get('features', []):
                img_id = img.get('id')
                props = img.get('properties', {})
                timestamp_ms = props.get('system:time_start', 0)
                captured_at = datetime.fromtimestamp(timestamp_ms / 1000.0, tz=timezone.utc)
                
                # Approximate geometry string
                wkt = f"POLYGON(({bbox.min_lon} {bbox.min_lat}, {bbox.max_lon} {bbox.min_lat}, {bbox.max_lon} {bbox.max_lat}, {bbox.min_lon} {bbox.max_lat}, {bbox.min_lon} {bbox.min_lat}))"
                
                scenes.append(SatelliteScene(
                    scene_id=img_id,
                    provider=self.provider_id(),
                    captured_at=captured_at,
                    bbox=bbox,
                    cloud_cover=props.get('CLOUDY_PIXEL_PERCENTAGE', 0.0),
                    resolution_meters=10.0,
                    bands=COLLECTION_BANDS[GEECollection.SENTINEL_2_OPTICAL],
                    geometry=wkt,
                    metadata={"index": props.get('system:index')}
                ))
            
            wkt = f"POLYGON(({bbox.min_lon} {bbox.min_lat}, {bbox.max_lon} {bbox.min_lat}, {bbox.max_lon} {bbox.max_lat}, {bbox.min_lon} {bbox.max_lat}, {bbox.min_lon} {bbox.min_lat}))"
            
            return SatelliteTimeseries(
                provider=self.provider_id(),
                location_wkt=wkt,
                start_time=start_time,
                end_time=end_time,
                scenes=scenes
            )

        return await GEEClient.execute(_fetch_collection)

    async def fetch_metadata(self) -> SatelliteMetadata:
        return SatelliteMetadata(
            provider=self.provider_id(),
            metadata={
                "collections_supported": [c.value for c in GEECollection],
                "api": "earthengine-api"
            }
        )
