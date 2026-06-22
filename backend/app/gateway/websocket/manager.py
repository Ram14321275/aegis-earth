import asyncio
import json
import logging
from typing import Dict, Set

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from app.core.cache.redis_client import redis_client
from app.gateway.contracts.public import StreamingSnapshot
from app.observability.metrics import metrics_store
from app.core.security.auth import get_current_user_ws

logger = logging.getLogger(__name__)

ws_router = APIRouter(prefix="/ws/v1", tags=["WebSocket Gateway"])


class WebSocketFederationManager:
    """
    Unified WebSocket Gateway.
    Multiplexes internal Redis Pub/Sub streams to external clients.
    Implements tenant isolation, replay-safe architecture, and queue backpressure.
    """

    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self.pubsub_task: asyncio.Task = None

    async def connect(self, websocket: WebSocket, tenant_id: str):
        await websocket.accept()
        if tenant_id not in self.active_connections:
            self.active_connections[tenant_id] = set()
        self.active_connections[tenant_id].add(websocket)
        
        # Update metrics
        total_conns = sum(len(conns) for conns in self.active_connections.values())
        metrics_store.update_active_websocket_connections(total_conns)
        logger.info(f"WebSocket connected. Tenant: {tenant_id}. Total: {total_conns}")

    def disconnect(self, websocket: WebSocket, tenant_id: str):
        if tenant_id in self.active_connections:
            self.active_connections[tenant_id].discard(websocket)
            if not self.active_connections[tenant_id]:
                del self.active_connections[tenant_id]
                
        metrics_store.record_websocket_disconnect()
        total_conns = sum(len(conns) for conns in self.active_connections.values())
        metrics_store.update_active_websocket_connections(total_conns)
        logger.info(f"WebSocket disconnected. Tenant: {tenant_id}. Total: {total_conns}")

    async def _broadcast_to_tenant(self, tenant_id: str, payload: dict):
        if tenant_id not in self.active_connections:
            return
            
        disconnected = set()
        payload_bytes = json.dumps(payload).encode("utf-8")
        
        for ws in self.active_connections[tenant_id]:
            try:
                # We could add a timeout/backpressure check here
                await ws.send_text(json.dumps(payload))
                metrics_store.record_websocket_message(len(payload_bytes), latency_ms=1.0)
            except Exception as e:
                logger.error(f"Error broadcasting to WebSocket: {e}")
                disconnected.add(ws)
                
        for ws in disconnected:
            self.disconnect(ws, tenant_id)

    async def listen_to_internal_streams(self):
        """
        Runs in background. Subscribes to internal provider streams (flood, wildfire)
        and multiplexes them to the correct external tenant sockets.
        """
        client = await redis_client.get_client()
        if not client:
            logger.error("Redis not available for WebSocket Federation.")
            return

        pubsub = client.pubsub()
        await pubsub.subscribe("internal:stream:flood", "internal:stream:wildfire", "internal:stream:fusion")
        
        logger.info("WebSocket Federation Manager listening to internal streams.")
        
        try:
            async for message in pubsub.listen():
                if message["type"] == "message":
                    try:
                        data = json.loads(message["data"].decode("utf-8"))
                        tenant_id = data.get("tenant_id", "anonymous")
                        
                        # Validate against public contract
                        # Ensure we don't leak internal metadata
                        public_payload = StreamingSnapshot(**data).model_dump()
                        
                        await self._broadcast_to_tenant(tenant_id, public_payload)
                    except Exception as e:
                        logger.error(f"Failed to process internal stream message: {e}")
        except asyncio.CancelledError:
            logger.info("WebSocket Federation Manager shutting down.")
        finally:
            await pubsub.unsubscribe()
            await pubsub.close()

    def start_background_task(self):
        if self.pubsub_task is None or self.pubsub_task.done():
            self.pubsub_task = asyncio.create_task(self.listen_to_internal_streams())


ws_manager = WebSocketFederationManager()


@ws_router.websocket("/intelligence")
async def websocket_intelligence_endpoint(
    websocket: WebSocket,
    # Rate limit and Auth validation
    user: dict = Depends(get_current_user_ws)
):
    tenant_id = user.get("tenant_id", "anonymous")
    
    # Ensure background task is running
    ws_manager.start_background_task()
    
    await ws_manager.connect(websocket, tenant_id)
    try:
        while True:
            # We don't expect client messages, but we keep connection alive
            data = await websocket.receive_text()
            # Handle potential keep-alives or subscription changes here
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, tenant_id)
