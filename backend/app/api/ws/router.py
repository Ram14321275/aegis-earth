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


