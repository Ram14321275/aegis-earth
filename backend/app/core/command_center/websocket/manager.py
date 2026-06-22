import asyncio
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class CommandCenterWebSocketManager:
    """
    Handles live planetary intelligence streams,
    timeline updates, and priority escalations over WebSockets.
    """

    def __init__(self):
        # Maps tenant_id -> list of active connections
        self.active_connections: Dict[str, list] = {}

    async def connect(self, tenant_id: str, websocket: Any):
        """
        Accepts a websocket connection for a tenant.
        """
        await websocket.accept()
        if tenant_id not in self.active_connections:
            self.active_connections[tenant_id] = []
        self.active_connections[tenant_id].append(websocket)
        logger.info(f"Command Center WS connected for tenant: {tenant_id}")

    def disconnect(self, tenant_id: str, websocket: Any):
        """
        Removes a connection.
        """
        if tenant_id in self.active_connections:
            if websocket in self.active_connections[tenant_id]:
                self.active_connections[tenant_id].remove(websocket)
            if not self.active_connections[tenant_id]:
                del self.active_connections[tenant_id]
        logger.info(f"Command Center WS disconnected for tenant: {tenant_id}")

    async def broadcast_timeline_delta(self, tenant_id: str, payload: Dict[str, Any]):
        """
        Sends delta updates to the timeline.
        """
        if tenant_id in self.active_connections:
            for connection in self.active_connections[tenant_id]:
                try:
                    await connection.send_json(payload)
                except Exception as e:
                    logger.error(f"Error sending delta to tenant {tenant_id}: {e}")
                    self.disconnect(tenant_id, connection)

command_center_ws_manager = CommandCenterWebSocketManager()
