from typing import Dict, Any, List
import logging
import uuid
import hashlib

from app.observability.metrics import metrics_store

logger = logging.getLogger(__name__)

class ThreatIntelligenceFeed:
    """Manages deterministic MVP threat indicators locally."""
    def __init__(self):
        self._indicators: Dict[str, Dict[str, Any]] = {}

    def ingest_ioc(self, value: str, ioc_type: str, confidence: float) -> str:
        """Deterministically normalizes and ingests an Indicator of Compromise."""
        indicator_id = f"ioc-{hashlib.sha256(value.encode()).hexdigest()[:12]}"
        
        self._indicators[indicator_id] = {
            "id": indicator_id,
            "value": value,
            "type": ioc_type,
            "confidence": confidence
        }
        logger.info(f"Ingested IOC {indicator_id} of type {ioc_type}")
        return indicator_id

    def check_ioc(self, value: str) -> bool:
        """Checks if a value matches a known indicator."""
        # O(N) scan for MVP, normally this would use a Bloom filter or indexed DB
        for ioc in self._indicators.values():
            if ioc["value"] == value:
                return True
        return False

intelligence_feed = ThreatIntelligenceFeed()
