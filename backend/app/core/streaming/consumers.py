import asyncio
import logging
from pydantic import ValidationError

from app.core.streaming.broker import streaming_broker
from app.core.streaming.events import ALL_STREAM_CHANNELS
from app.core.streaming.models import BaseStreamEvent
from app.core.streaming.websocket import websocket_manager

logger = logging.getLogger(__name__)

class EventConsumer:
    """
    Subscribes to global Redis Pub/Sub channels and routes events 
    to the local WebSocket Gateway for distribution.
    """
    
    def __init__(self):
        self._tasks: list[asyncio.Task] = []
        
    async def start(self):
        logger.info("Starting Streaming Consumers...")
        for channel in ALL_STREAM_CHANNELS:
            task = asyncio.create_task(self._listen(channel))
            self._tasks.append(task)
            
    async def stop(self):
        logger.info("Stopping Streaming Consumers...")
        for task in self._tasks:
            task.cancel()
        await asyncio.gather(*self._tasks, return_exceptions=True)
        self._tasks.clear()

    async def _listen(self, channel: str):
        try:
            async for raw_message in streaming_broker.subscribe(channel):
                try:
                    # Validate the envelope
                    event = BaseStreamEvent.parse_raw(raw_message)
                    # Dispatch to connected websockets
                    websocket_manager.broadcast_event(event)
                except ValidationError as e:
                    logger.error(f"Failed to parse event on {channel}: {e}")
                except Exception as e:
                    logger.error(f"Error broadcasting event from {channel}: {e}")
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Consumer loop failed for {channel}: {e}")

event_consumer = EventConsumer()
