from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List

from app.core.resilience.healing.engine import healing_engine
from app.core.resilience.stabilization.engine import stabilization_engine
from app.core.resilience.mesh.topology import resilience_mesh
from app.core.resilience.failover.promotion import failover_promoter
from app.core.resilience.verification.engine import verification_engine
from app.core.resilience.recovery.manager import recovery_manager
from app.core.resilience.degradation.modes import degradation_manager
from app.core.resilience.simulation.engine import resilience_simulation_engine

router = APIRouter(prefix="/resilience", tags=["resilience"])

@router.post("/healing/trigger")
async def trigger_healing(action_type: str, target: str):
    return healing_engine.trigger_healing(action_type, target)

@router.post("/recovery/start")
async def start_recovery(target_node: str, expected_region: str, checkpoints: List[Dict[str, Any]]):
    return recovery_manager.start_recovery(target_node, checkpoints, expected_region)

@router.post("/failover/promote")
async def promote_failover(old_primary: str, new_primary: str, primary_region: str, new_region: str):
    return failover_promoter.promote_node(old_primary, new_primary, primary_region, new_region)

@router.post("/stabilization/analyze")
async def analyze_stabilization(queue_depth: int, ws_connections: int, cpu_load: float):
    return stabilization_engine.generate_recommendations(queue_depth, ws_connections, cpu_load)

@router.post("/degradation/mode")
async def set_degradation_mode(mode: str):
    success = degradation_manager.transition_mode(mode)
    if not success:
        raise HTTPException(status_code=400, detail="Invalid degradation mode requested.")
    return {"status": "success", "current_mode": mode}

@router.post("/simulations/run")
async def run_simulation(scenario: str, parameters: Dict[str, Any]):
    return await resilience_simulation_engine.run_simulation(scenario, parameters)

@router.get("/mesh/health")
async def get_mesh_health():
    return {"mesh_survivability_score": resilience_mesh.calculate_mesh_health()}

@router.post("/verification/check")
async def verify_chain(expected_region: str, checkpoints: List[Dict[str, Any]]):
    valid = verification_engine.verify_restoration_chain(checkpoints, expected_region)
    return {"status": "VERIFIED" if valid else "ABORTED"}
