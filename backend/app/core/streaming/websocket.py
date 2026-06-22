import asyncio
import json
import logging
from typing import Dict, Any

from fastapi import WebSocket, WebSocketDisconnect
from pydantic import ValidationError

from app.core.streaming.models import ClientSubscription, BaseStreamEvent
from app.core.streaming.subscriptions import subscription_manager
from app.observability.metrics import metrics_store

logger = logging.getLogger(__name__)

# Constants for abuse protection
MAX_PAYLOAD_SIZE_BYTES = 64 * 1024  # 64KB
MAX_SUBSCRIPTIONS = 100
MAX_OUTBOUND_QUEUE_SIZE = 500  # Backpressure limit


class ConnectionContext:
    def __init__(self, websocket: WebSocket, connection_id: str):
        self.websocket = websocket
        self.connection_id = connection_id
        # Bounded asyncio queue for backpressure safety
        self.queue: asyncio.Queue[str] = asyncio.Queue(maxsize=MAX_OUTBOUND_QUEUE_SIZE)
        self._sender_task: asyncio.Task | None = None
        
    async def start_sender(self):
        self._sender_task = asyncio.create_task(self._send_loop())
        
    async def stop_sender(self):
        if self._sender_task:
            self._sender_task.cancel()
            
    async def _send_loop(self):
        try:
            while True:
                message = await self.queue.get()
                await self.websocket.send_text(message)
                self.queue.task_done()
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Sender loop failed for {self.connection_id}: {str(e)}")

    def enqueue(self, message: str) -> bool:
        """
        Attempts to enqueue a message. Returns False if queue is full (slow client).
        """
        try:
            self.queue.put_nowait(message)
            return True
        except asyncio.QueueFull:
            return False


class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, ConnectionContext] = {}

    async def connect(self, websocket: WebSocket) -> str:
        await websocket.accept()
        connection_id = f"conn_{id(websocket)}"
        ctx = ConnectionContext(websocket, connection_id)
        self.active_connections[connection_id] = ctx
        await ctx.start_sender()
        
        metrics_store.update_active_websocket_connections(len(self.active_connections))
        logger.info(f"WebSocket connected: {connection_id}")
        return connection_id

    async def disconnect(self, connection_id: str, is_backpressure: bool = False):
        if connection_id in self.active_connections:
            ctx = self.active_connections.pop(connection_id)
            await ctx.stop_sender()
            subscription_manager.remove_subscription(connection_id)
            
            try:
                # 1008 = Policy Violation, 1000 = Normal Closure
                code = 1008 if is_backpressure else 1000
                await ctx.websocket.close(code=code)
            except Exception:
                pass
                
            metrics_store.update_active_websocket_connections(len(self.active_connections))
            metrics_store.record_websocket_disconnect(is_backpressure=is_backpressure)
            logger.info(f"WebSocket disconnected: {connection_id} (Backpressure: {is_backpressure})")

    async def process_client_message(self, connection_id: str, message: str):
        # 1. Payload size check
        size_bytes = len(message.encode("utf-8"))
        if size_bytes > MAX_PAYLOAD_SIZE_BYTES:
            logger.warning(f"Connection {connection_id} exceeded max payload size.")
            await self.disconnect(connection_id, is_backpressure=True)
            return

        metrics_store.record_websocket_message(size_bytes)
        
        # 2. Parse subscription
        try:
            data = json.loads(message)
            if data.get("action") == "subscribe":
                # Only extract up to MAX_SUBSCRIPTIONS (e.g. max regions)
                payload = data.get("payload", {})
                
                # Bounding abuse
                if len(payload.get("regions", [])) > MAX_SUBSCRIPTIONS:
                    payload["regions"] = payload["regions"][:MAX_SUBSCRIPTIONS]
                    
                sub = ClientSubscription(**payload)
                subscription_manager.set_subscription(connection_id, sub)
                logger.info(f"Updated subscription for {connection_id}: {sub.dict()}")
                
                # Send ACK via enqueue
                self._safe_enqueue(connection_id, json.dumps({"status": "subscribed", "message": "Subscription updated."}))
                
            elif data.get("action") == "ping":
                self._safe_enqueue(connection_id, json.dumps({"action": "pong"}))
                
        except json.JSONDecodeError:
            logger.warning(f"Connection {connection_id} sent malformed JSON.")
        except ValidationError as e:
            logger.warning(f"Connection {connection_id} sent invalid subscription: {e}")

    def _safe_enqueue(self, connection_id: str, message: str):
        if connection_id in self.active_connections:
            ctx = self.active_connections[connection_id]
            success = ctx.enqueue(message)
            if not success:
                metrics_store.record_websocket_queue_overflow()
                logger.warning(f"Slow client {connection_id}. Outbound queue overflow. Disconnecting.")
                # Disconnect the slow client in the background to avoid blocking
                asyncio.create_task(self.disconnect(connection_id, is_backpressure=True))

    def broadcast_event(self, event: BaseStreamEvent):
        """
        Filters and routes an internal event to appropriate connected clients.
        Does NOT block if clients are slow.
        """
        msg_str = event.json()
        
        for connection_id, ctx in list(self.active_connections.items()):
            if subscription_manager.should_dispatch(connection_id, event):
                self._safe_enqueue(connection_id, msg_str)

websocket_manager = WebSocketManager()
