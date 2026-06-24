from typing import Dict, Any
import logging
import uuid
import hashlib

from app.observability.metrics import metrics_store

logger = logging.getLogger(__name__)

class MarketSignalEngine:
    """Deterministic market signal ingestion without opaque speculative AI."""
    
    def ingest_signal(self, signal_type: str, volatility: float, staleness_seconds: float) -> Dict[str, Any]:
        """Ingests a market signal and calculates confidence based on staleness."""
        
        # Confidence degrades linearly based on staleness (e.g. loses 1% confidence every 60 seconds)
        confidence = max(0.0, 1.0 - (staleness_seconds / 6000.0))
        
        reasoning = f"type:{signal_type}|vol:{volatility}|stale:{staleness_seconds}=>{confidence}"
        reasoning_hash = hashlib.sha256(reasoning.encode()).hexdigest()
        
        if volatility > 0.8:
            metrics_store.record_economic_action("market_instability_events_total")
            
        return {
            "signal_id": f"sig-{uuid.uuid4()}",
            "type": signal_type,
            "volatility": volatility,
            "staleness_seconds": staleness_seconds,
            "confidence_score": confidence,
            "reasoning_hash": reasoning_hash
        }

market_signal_engine = MarketSignalEngine()
