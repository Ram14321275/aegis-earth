import time
from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel

from app.core.security.auth import get_current_user_optional
from app.core.command_center.timeline.engine import global_timeline_engine
from app.core.command_center.snapshots.engine import snapshot_engine
from app.core.command_center.exports.service import command_center_export_service
from app.schemas.command_center import GlobalThreatSummary, TimelineSnapshot
from app.observability.metrics import metrics_store

router = APIRouter(prefix="/command-center", tags=["Planetary Command Center"])

class ExportRequest(BaseModel):
    snapshot_id: str
    format: str

@router.get("/timeline", response_model=GlobalThreatSummary)
async def get_timeline(
    window: str = "24h",
    force_dynamic: bool = False,
    user: Any = Depends(get_current_user_optional)
):
    start_time = time.time()
    tenant_id = user.get("tenant_id") if user else "anonymous"

    if window not in ["1h", "24h", "7d", "30d", "90d"]:
        raise HTTPException(status_code=400, detail="Invalid window type")

    summary = await global_timeline_engine.generate_timeline(tenant_id, window, force_dynamic)

    # Observability
    duration_ms = (time.time() - start_time) * 1000
    metrics_store.record_command_center_action("timeline_generation_duration_ms", duration_ms)
    metrics_store.record_command_center_action("timeline_queries_total", 1)

    return summary

@router.get("/priorities")
async def get_priorities(
    user: Any = Depends(get_current_user_optional)
):
    """
    Returns global threat priorities (hotspots sorted by deterministic ranking).
    """
    tenant_id = user.get("tenant_id") if user else "anonymous"
    # Reusing timeline engine to get hotspots for MVP
    summary = await global_timeline_engine.generate_timeline(tenant_id, "24h", False)
    
    all_hotspots = []
    for region in summary.critical_regions:
        all_hotspots.extend(region.active_hotspots)
        
    # Sort descending by threat score
    all_hotspots.sort(key=lambda x: x.threat_score, reverse=True)
    return {"priorities": all_hotspots}

@router.post("/export", status_code=202)
async def request_export(
    request: ExportRequest,
    user: Any = Depends(get_current_user_optional)
):
    tenant_id = user.get("tenant_id") if user else "anonymous"
    
    try:
        job_id = await command_center_export_service.request_export(
            tenant_id=tenant_id, 
            snapshot_id=request.snapshot_id, 
            format_type=request.format
        )
        metrics_store.record_command_center_action("export_jobs_total", 1)
        return {"job_id": job_id, "status": "accepted"}
    except HTTPException as e:
        raise e
    except Exception as e:
        metrics_store.record_command_center_action("export_failures_total", 1)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/export/{job_id}")
async def get_export_status(
    job_id: str,
    user: Any = Depends(get_current_user_optional)
):
    tenant_id = user.get("tenant_id") if user else "anonymous"
    
    status = await command_center_export_service.get_export_status(tenant_id, job_id)
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
        
    return status

@router.get("/snapshots/{snapshot_id}", response_model=TimelineSnapshot)
async def get_snapshot(
    snapshot_id: str,
    user: Any = Depends(get_current_user_optional)
):
    tenant_id = user.get("tenant_id") if user else "anonymous"
    
    snapshot = await snapshot_engine.get_snapshot(snapshot_id)
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")
        
    if snapshot.tenant_id != tenant_id:
        raise HTTPException(status_code=403, detail="Access denied")
        
    return snapshot
