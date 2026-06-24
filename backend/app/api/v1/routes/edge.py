from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List

from app.core.edge.topology.registry import edge_registry
from app.core.edge.topology.models import EdgeNodeConfig
from app.core.edge.synchronization.orchestrator import sync_orchestrator
from app.core.edge.failover.manager import failover_manager
from app.core.edge.recovery.engine import recovery_engine
from app.core.edge.degraded.engine import degraded_engine
from app.core.edge.sovereignty.partitioning import partition_manager

router = APIRouter(prefix="/edge", tags=["edge"])

@router.post("/nodes/register")
async def register_edge_node(config: EdgeNodeConfig):
    """Register a new edge node in the topology."""
    state = edge_registry.register_node(config)
    return {"status": "success", "node_state": state.dict()}

@router.get("/topology")
async def get_topology():
    """Retrieve edge topology status."""
    return {"nodes": [state.dict() for state in edge_registry._nodes.values()]}

@router.post("/nodes/{node_id}/heartbeat")
async def edge_heartbeat(node_id: str, health_state: str):
    """Update heartbeat for an edge node."""
    edge_registry.update_heartbeat(node_id, health_state)
    return {"status": "ok"}

@router.post("/synchronization/batch")
async def process_sync_batch(node_id: str, events: List[Dict[str, Any]]):
    """Process a batch of sync events from an edge node."""
    success = await sync_orchestrator.process_sync_batch(node_id, events)
    if not success:
        raise HTTPException(status_code=400, detail="Synchronization rejected due to lineage divergence.")
    return {"status": "synchronized", "events_processed": len(events)}

@router.post("/failover/initiate")
async def initiate_failover(failed_node_id: str, region: str, fallback_node_id: str):
    """Initiate regional failover."""
    await failover_manager.handle_node_failure(failed_node_id, region, fallback_node_id)
    return {"status": "failover_initiated"}

@router.post("/recovery/initiate")
async def initiate_recovery(node_id: str):
    """Recover an offline node."""
    success = await recovery_engine.initiate_recovery(node_id)
    if not success:
        raise HTTPException(status_code=500, detail="Recovery failed. Manual intervention required.")
    return {"status": "recovery_successful"}

@router.get("/sovereignty/partitions")
async def get_sovereign_partitions(tenant_id: str):
    """Retrieve allowed partitions for a tenant."""
    allowed = partition_manager.get_allowed_partitions(tenant_id)
    return {"tenant_id": tenant_id, "allowed_partitions": allowed}
