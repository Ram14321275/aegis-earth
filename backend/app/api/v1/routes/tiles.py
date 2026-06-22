import time
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Response

from app.core.security.auth import get_current_user_optional
from app.core.tiles.vector.engine import vector_tile_engine
from app.core.tiles.raster.engine import raster_tile_engine
from app.core.tiles.caching.edge import edge_cache_manager
from app.observability.metrics import metrics_store

router = APIRouter(prefix="/tiles", tags=["Geospatial Visualization"])

@router.get("/vector/{hazard_type}/{z}/{x}/{y}")
async def get_vector_tile(
    hazard_type: str,
    z: int,
    x: int,
    y: int,
    response: Response,
    user: Any = Depends(get_current_user_optional)
):
    start_time = time.time()
    tenant_id = user.get("tenant_id") if user else "anonymous"

    tile_bytes = await vector_tile_engine.get_hazard_tile(tenant_id, hazard_type, z, x, y)
    
    if not tile_bytes:
        raise HTTPException(status_code=404, detail="Tile not found or empty")

    duration_ms = (time.time() - start_time) * 1000
    metrics_store.record_tile_generation(duration_ms, "vector", len(tile_bytes))

    # Apply CDN edge cache headers based on MVP severity assumption
    # In production, hazard severity would be fetched to dictate TTL dynamically
    edge_cache_manager.set_tile_cache_headers(response, severity="HIGH", payload_bytes=tile_bytes)
    
    # application/x-protobuf for MVT
    return Response(content=tile_bytes, media_type="application/x-protobuf")


@router.get("/raster/{hazard_type}/{z}/{x}/{y}")
async def get_raster_tile(
    hazard_type: str,
    z: int,
    x: int,
    y: int,
    response: Response,
    format: str = "png",
    user: Any = Depends(get_current_user_optional)
):
    start_time = time.time()
    tenant_id = user.get("tenant_id") if user else "anonymous"

    tile_bytes = await raster_tile_engine.get_raster_tile(tenant_id, hazard_type, z, x, y, format)
    
    if not tile_bytes:
        raise HTTPException(status_code=404, detail="Raster tile generation failed")

    duration_ms = (time.time() - start_time) * 1000
    metrics_store.record_tile_generation(duration_ms, "raster", len(tile_bytes))

    edge_cache_manager.set_tile_cache_headers(response, severity="HIGH", payload_bytes=tile_bytes)
    
    media_type = "image/webp" if format.lower() == "webp" else "image/png"
    return Response(content=tile_bytes, media_type=media_type)


@router.get("/playback/{hazard_type}")
async def get_playback_timeline(
    hazard_type: str,
    start_time: str,
    end_time: str,
    user: Any = Depends(get_current_user_optional)
):
    from app.core.tiles.playback.timeline import playback_timeline
    from datetime import datetime
    
    try:
        st = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        et = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ISO8601 timestamps")

    frames = await playback_timeline.get_timeline_frames(hazard_type, st, et)
    return {"hazard_type": hazard_type, "frames": frames}
