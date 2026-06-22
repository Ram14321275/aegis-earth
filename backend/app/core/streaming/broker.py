import asyncio
import logging
from abc import ABC, abstractmethod
from typing import AsyncIterator, Callable, Awaitable

from app.core.cache.redis_client import redis_client
from app.observability.metrics import metrics_store

logger = logging.getLogger(__name__)

class StreamingBroker(ABC):
    """
    Abstract streaming broker interface to allow future drop-in replacement 
    (e.g., migrating from Redis to Kafka/NATS) without rewriting the WebSocket Gateway.
    """
    @abstractmethod
    async def publish(self, channel: str, message: str) -> bool:
        """Publishes a serialized message to a channel."""
        pass

    @abstractmethod
    async def subscribe(self, channel: str) -> AsyncIterator[str]:
        """Yields messages from a channel."""
        pass


class RedisPubSubBroker(StreamingBroker):
    async def publish(self, channel: str, message: str) -> bool:
        client = await redis_client.get_client()
        if not client:
            metrics_store.record_pubsub_failure()
            logger.error(f"Failed to acquire Redis client for publishing to {channel}")
            return False
            
        try:
            await client.publish(channel, message)
            return True
        except Exception as e:
            metrics_store.record_pubsub_failure()
            logger.error(f"Failed to publish to {channel}: {str(e)}")
            return False

    async def subscribe(self, channel: str) -> AsyncIterator[str]:
        client = await redis_client.get_client()
        if not client:
            metrics_store.record_pubsub_failure()
            logger.error("Failed to acquire Redis client for subscription.")
            return
            
        pubsub = client.pubsub()
        try:
            await pubsub.subscribe(channel)
            logger.info(f"Subscribed to Redis channel: {channel}")
            
            async for message in pubsub.listen():
                if message["type"] == "message":
                    yield message["data"]
        except asyncio.CancelledError:
            logger.info(f"Unsubscribing from {channel} due to cancellation.")
            raise
        except Exception as e:
            metrics_store.record_pubsub_failure()
            logger.error(f"Error while listening to {channel}: {str(e)}")
            raise e
        finally:
            await pubsub.unsubscribe(channel)
            await pubsub.close()

streaming_broker = RedisPubSubBroker()
