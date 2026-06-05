import json
import time
from datetime import datetime
from typing import List

from app.core.geospatial.models import BoundingBox
from app.core.satellite.models import SatelliteScene, SatelliteTimeseries
from app.core.satellite.registry import satellite_registry
from app.core.satellite.validators import validate_timeseries_request
from app.core.cache.manager import cache_manager
from app.observability.metrics import metrics_store

class SatelliteService:
    async def fetch_scene(self, provider_id: str, scene_id: str) -> SatelliteScene:
        provider = satellite_registry.get_provider(provider_id)
        if not provider:
            raise ValueError(f"Provider not found: {provider_id}")

        cache_key = f"satellite:scene:{provider_id}:{scene_id}"
        cached_data = await cache_manager.get(cache_key)
        
        if cached_data:
            metrics_store.record_satellite_request(cache_hit=True, success=True, duration_ms=0.0)
            data_dict = json.loads(cached_data)
            return SatelliteScene.model_validate(data_dict)

        start_time = time.time()
        try:
            scene = await provider.fetch_scene(scene_id)
            duration_ms = (time.time() - start_time) * 1000
            metrics_store.record_satellite_request(cache_hit=False, success=True, duration_ms=duration_ms)
            
            # Cache for 6 hours
            await cache_manager.set(cache_key, scene.model_dump_json(), ttl=21600)
            return scene
        except Exception as e:
            metrics_store.record_satellite_request(cache_hit=False, success=False, duration_ms=0.0)
            raise e

    async def fetch_timeseries(
        self, provider_id: str, bbox: BoundingBox, start_time: datetime, end_time: datetime
    ) -> SatelliteTimeseries:
        validate_timeseries_request(start_time, end_time)
        
        provider = satellite_registry.get_provider(provider_id)
        if not provider:
            raise ValueError(f"Provider not found: {provider_id}")

        # Basic cache key based on bounding box constraints and time
        bbox_hash = f"{bbox.min_lon}_{bbox.min_lat}_{bbox.max_lon}_{bbox.max_lat}"
        cache_key = f"satellite:timeseries:{provider_id}:{bbox_hash}:{start_time.isoformat()}:{end_time.isoformat()}"
        
        cached_data = await cache_manager.get(cache_key)
        if cached_data:
            metrics_store.record_satellite_request(cache_hit=True, success=True, duration_ms=0.0)
            return SatelliteTimeseries.model_validate(json.loads(cached_data))

        start_timer = time.time()
        try:
            timeseries = await provider.fetch_timeseries(bbox, start_time, end_time)
            duration_ms = (time.time() - start_timer) * 1000
            metrics_store.record_satellite_request(cache_hit=False, success=True, duration_ms=duration_ms)
            
            # Cache for 1 hour
            await cache_manager.set(cache_key, timeseries.model_dump_json(), ttl=3600)
            return timeseries
        except Exception as e:
            metrics_store.record_satellite_request(cache_hit=False, success=False, duration_ms=0.0)
            raise e

satellite_service = SatelliteService()
