import json
import logging
from typing import Dict, Any

from app.gateway.websocket.manager import ws_manager

logger = logging.getLogger(__name__)

class LiveTileStreaming:
    """
    Handles granular viewport-scoped invalidations over WebSockets.
    """

    @staticmethod
    async def broadcast_invalidation(tenant_id: str, hazard_type: str, z: int, x: int, y: int, reason: str = "update"):
        """
        Pushes a tile invalidation event to the WebSocket federation layer.
        """
        payload = {
            "type": "tile_invalidation",
            "layer": hazard_type,
            "z": z,
            "x": x,
            "y": y,
            "reason": reason,
            "tile_version": "v2" # Mock version logic
        }
        
        try:
            # Push via the websocket federation manager to specific tenant
            await ws_manager._broadcast_to_tenant(tenant_id, payload)
        except Exception as e:
            logger.error(f"Failed to broadcast live tile invalidation: {e}")

live_tile_streaming = LiveTileStreaming()
