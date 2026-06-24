from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List

from app.core.cyber.detection.engine import detection_engine, ReasonCode
from app.core.cyber.containment.engine import containment_engine
from app.core.cyber.quarantine.manager import quarantine_manager
from app.core.cyber.zero_trust.fabric import zero_trust_fabric
from app.core.cyber.attestation.verifier import attestation_verifier
from app.core.cyber.intelligence.feed import intelligence_feed
from app.core.cyber.forensics.engine import forensic_engine
from app.core.cyber.replay.session import replay_session_manager
from app.core.cyber.simulation.engine import simulation_engine

router = APIRouter(prefix="/cyber", tags=["cyber"])

@router.post("/signals/evaluate")
async def evaluate_threat_signals(signals: List[ReasonCode], staleness_seconds: float = 0.0):
    return detection_engine.evaluate_threat(signals, staleness_seconds)

@router.post("/containment/trigger")
async def trigger_containment(action_type: str, target_id: str, lineage_hash: str, enterprise_tenant: bool = False):
    return containment_engine.trigger_containment(action_type, target_id, lineage_hash, enterprise_tenant)

@router.post("/quarantine/start")
async def start_quarantine(target_id: str, reason: str):
    session_id = quarantine_manager.start_quarantine(target_id, reason)
    return {"status": "quarantined", "session_id": session_id}

@router.post("/quarantine/lift")
async def lift_quarantine(target_id: str):
    quarantine_manager.lift_quarantine(target_id)
    return {"status": "lifted"}

@router.post("/zero-trust/validate")
async def validate_zero_trust(source_id: str, nonce: str, request_counter: int):
    valid = zero_trust_fabric.validate_request_lineage(source_id, nonce, request_counter)
    if not valid:
        raise HTTPException(status_code=403, detail="Zero Trust Failure: Replay or Lineage Invalid")
    return {"status": "valid"}

@router.post("/attestation/verify")
async def verify_attestation(node_id: str, nonce: str, signature: str):
    valid = attestation_verifier.verify_attestation(node_id, nonce, signature)
    if not valid:
        raise HTTPException(status_code=403, detail="Attestation Verification Failed")
    return {"status": "verified"}

@router.post("/intelligence/ingest")
async def ingest_intelligence(value: str, ioc_type: str, confidence: float):
    ioc_id = intelligence_feed.ingest_ioc(value, ioc_type, confidence)
    return {"status": "ingested", "indicator_id": ioc_id}

@router.post("/forensics/reconstruct")
async def reconstruct_forensics(incident_id: str, events: List[Dict[str, Any]]):
    return forensic_engine.reconstruct_attack_timeline(incident_id, events)

@router.post("/simulations/run")
async def run_simulation(scenario: str, parameters: Dict[str, Any]):
    return await simulation_engine.run_simulation(scenario, parameters)

# Placeholder GET routes for resources
@router.get("/incidents")
async def get_incidents():
    return {"incidents": []}

@router.get("/threats")
async def get_threats():
    return {"threats": list(intelligence_feed._indicators.values())}
