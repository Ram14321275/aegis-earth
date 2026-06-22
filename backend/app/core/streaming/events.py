from enum import Enum

class StreamChannel(str, Enum):
    """
    Standardized channel routing keys for Redis Pub/Sub streams.
    Critical for future distributed scale and Kafka migration.
    """
    FLOOD = "stream:flood"
    WILDFIRE = "stream:wildfire"
    ENVIRONMENTAL = "stream:environmental"
    INTELLIGENCE = "stream:intelligence"
    ALERTS = "stream:alerts"
    SYSTEM = "stream:system"

ALL_STREAM_CHANNELS = [
    StreamChannel.FLOOD,
    StreamChannel.WILDFIRE,
    StreamChannel.ENVIRONMENTAL,
    StreamChannel.INTELLIGENCE,
    StreamChannel.ALERTS,
    StreamChannel.SYSTEM,
]
