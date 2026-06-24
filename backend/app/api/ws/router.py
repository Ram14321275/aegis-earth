from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import logging
from app.core.streaming.websocket import websocket_manager
from app.core.streaming.models import ClientSubscription, StreamEventType

logger = logging.getLogger(__name__)
ws_router = APIRouter()

async def generic_ws_handler(websocket: WebSocket, default_category: StreamEventType = None):
    """
    Handles the WebSocket lifecycle.
    Can be pre-configured with a default intelligence category.
    """
    connection_id = await websocket_manager.connect(websocket)
    
    try:
        # Pre-seed a basic subscription based on the endpoint they connected to
        from app.core.streaming.subscriptions import subscription_manager
        if default_category:
            sub = ClientSubscription(intelligence_categories=[default_category])
            subscription_manager.set_subscription(connection_id, sub)
            
        while True:
            # Receive client messages (pings or dynamic subscription updates)
            message = await websocket.receive_text()
            await websocket_manager.process_client_message(connection_id, message)
            
    except WebSocketDisconnect:
        # Client gracefully or ungracefully disconnected
        await websocket_manager.disconnect(connection_id)
    except Exception as e:
        logger.error(f"WebSocket error on {connection_id}: {e}")
        await websocket_manager.disconnect(connection_id)


@ws_router.websocket("/intelligence")
async def websocket_intelligence(websocket: WebSocket):
    """
    Global intelligence stream.
    """
    await generic_ws_handler(websocket, default_category=StreamEventType.INTELLIGENCE)


@ws_router.websocket("/alerts")
async def websocket_alerts(websocket: WebSocket):
    """
    Tactical alerts stream.
    """
    await generic_ws_handler(websocket, default_category=StreamEventType.ALERT)


@ws_router.websocket("/system")
async def websocket_system(websocket: WebSocket):
    """
    System and platform telemetry stream.
    """
    await generic_ws_handler(websocket)

@ws_router.websocket("/providers")
async def websocket_providers(websocket: WebSocket):
    """
    Provider degradation streaming.
    """
    await generic_ws_handler(websocket, default_category=StreamEventType.PROVIDERS)

@ws_router.websocket("/integrations")
async def websocket_integrations(websocket: WebSocket):
    """
    Ingestion alerts and replay notifications.
    """
    await generic_ws_handler(websocket, default_category=StreamEventType.INTEGRATIONS)

@ws_router.websocket("/humanitarian")
async def websocket_humanitarian(websocket: WebSocket):
    """
    Humanitarian coordination updates.
    """
    await generic_ws_handler(websocket, default_category=StreamEventType.HUMANITARIAN)

@ws_router.websocket("/distribution")
async def websocket_distribution(websocket: WebSocket):
    """
    Outbound delivery updates.
    """
    await generic_ws_handler(websocket, default_category=StreamEventType.DISTRIBUTION)

@ws_router.websocket("/governance")
async def websocket_governance(websocket: WebSocket):
    """Governance policies and violation updates."""
    await generic_ws_handler(websocket, default_category=StreamEventType.GOVERNANCE)

@ws_router.websocket("/audit")
async def websocket_audit(websocket: WebSocket):
    """Audit chain streaming."""
    await generic_ws_handler(websocket, default_category=StreamEventType.AUDIT)

@ws_router.websocket("/compliance")
async def websocket_compliance(websocket: WebSocket):
    """Compliance export status."""
    await generic_ws_handler(websocket, default_category=StreamEventType.COMPLIANCE)

@ws_router.websocket("/approvals")
async def websocket_approvals(websocket: WebSocket):
    """Approval workflow updates."""
    await generic_ws_handler(websocket, default_category=StreamEventType.APPROVALS)

@ws_router.websocket("/replay")
async def websocket_replay(websocket: WebSocket):
    """Replay session streaming."""
    await generic_ws_handler(websocket, default_category=StreamEventType.REPLAY)

@ws_router.websocket("/edge")
async def websocket_edge(websocket: WebSocket):
    """General edge operations streaming."""
    # Mapping to a catch-all edge type for general updates, or DEGRADED_MODE
    await generic_ws_handler(websocket, default_category=StreamEventType.DEGRADED_MODE)

@ws_router.websocket("/synchronization")
async def websocket_synchronization(websocket: WebSocket):
    """Edge synchronization status and checkpoints."""
    await generic_ws_handler(websocket, default_category=StreamEventType.SYNC_CHECKPOINT)

@ws_router.websocket("/failover")
async def websocket_failover(websocket: WebSocket):
    """Failover and election events."""
    await generic_ws_handler(websocket, default_category=StreamEventType.EDGE_FAILOVER)

@ws_router.websocket("/topology")
async def websocket_topology(websocket: WebSocket):
    """Edge topology and heartbeat updates."""
    # Mapping topology to edge failover/recovery conceptually
    await generic_ws_handler(websocket, default_category=StreamEventType.EDGE_RECOVERY)
# ==========================================
# Cyber Defense & Zero-Trust Federation
# ==========================================

@router.websocket("/ws/cyber")
async def websocket_cyber_endpoint(websocket: WebSocket):
    await manager.connect(websocket, "cyber")
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(websocket, "cyber")

@router.websocket("/ws/incidents")
async def websocket_incidents_endpoint(websocket: WebSocket):
    await manager.connect(websocket, "incidents")
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(websocket, "incidents")

@router.websocket("/ws/threats")
async def websocket_threats_endpoint(websocket: WebSocket):
    await manager.connect(websocket, "threats")
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(websocket, "threats")

@router.websocket("/ws/containment")
async def websocket_containment_endpoint(websocket: WebSocket):
    await manager.connect(websocket, "containment")
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(websocket, "containment")

@router.websocket("/ws/quarantine")
async def websocket_quarantine_endpoint(websocket: WebSocket):
    await manager.connect(websocket, "quarantine")
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(websocket, "quarantine")

@router.websocket("/ws/forensics")
async def websocket_forensics_endpoint(websocket: WebSocket):
    await manager.connect(websocket, "forensics")
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(websocket, "forensics")

@router.websocket("/ws/attestation")
async def websocket_attestation_endpoint(websocket: WebSocket):
    await manager.connect(websocket, "attestation")
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(websocket, "attestation")

# ==========================================
# Autonomous Sovereign Resilience & Mesh
# ==========================================

@router.websocket("/ws/resilience")
async def websocket_resilience_endpoint(websocket: WebSocket):
    await manager.connect(websocket, "resilience")
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(websocket, "resilience")

@router.websocket("/ws/recovery")
async def websocket_recovery_endpoint(websocket: WebSocket):
    await manager.connect(websocket, "recovery")
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(websocket, "recovery")

@router.websocket("/ws/failover")
async def websocket_failover_endpoint(websocket: WebSocket):
    await manager.connect(websocket, "failover")
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(websocket, "failover")

@router.websocket("/ws/healing")
async def websocket_healing_endpoint(websocket: WebSocket):
    await manager.connect(websocket, "healing")
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(websocket, "healing")

@router.websocket("/ws/mesh")
async def websocket_mesh_endpoint(websocket: WebSocket):
    await manager.connect(websocket, "mesh")
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(websocket, "mesh")

@router.websocket("/ws/stabilization")
async def websocket_stabilization_endpoint(websocket: WebSocket):
    await manager.connect(websocket, "stabilization")
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(websocket, "stabilization")

@router.websocket("/ws/degradation")
async def websocket_degradation_endpoint(websocket: WebSocket):
    await manager.connect(websocket, "degradation")
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(websocket, "degradation")
@ws_router.websocket("/reconciliation")
async def websocket_reconciliation(websocket: WebSocket):
    """Conflict reconciliation audit trails."""
    await generic_ws_handler(websocket, default_category=StreamEventType.RECONCILIATION_EVENT)

@ws_router.websocket("/recovery")
async def websocket_edge_recovery(websocket: WebSocket):
    """Offline node recovery updates."""
    await generic_ws_handler(websocket, default_category=StreamEventType.OFFLINE_RECOVERY)



