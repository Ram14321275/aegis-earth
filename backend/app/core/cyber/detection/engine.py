from typing import Dict, Any, List
import logging
from enum import Enum
import hashlib

from app.observability.metrics import metrics_store

logger = logging.getLogger(__name__)

class ReasonCode(str, Enum):
    REPLAY_NONCE_REUSE = "REPLAY_NONCE_REUSE"
    ABNORMAL_PROVIDER_DRIFT = "ABNORMAL_PROVIDER_DRIFT"
    WEBSOCKET_FLOOD_PATTERN = "WEBSOCKET_FLOOD_PATTERN"
    EDGE_ATTESTATION_FAILURE = "EDGE_ATTESTATION_FAILURE"
    GEO_ROUTING_IMPOSSIBLE = "GEO_ROUTING_IMPOSSIBLE"
    PRIVILEGE_ESCALATION_ATTEMPT = "PRIVILEGE_ESCALATION_ATTEMPT"
    AUDIT_CHAIN_CORRUPTION = "AUDIT_CHAIN_CORRUPTION"
    SYNCHRONIZATION_TAMPERING = "SYNCHRONIZATION_TAMPERING"

class CyberDetectionEngine:
    """Deterministic threat scoring without opaque ML logic."""
    
    def __init__(self):
        # Weights for deterministic scoring
        self.signal_weights = {
            ReasonCode.REPLAY_NONCE_REUSE: 0.9,
            ReasonCode.ABNORMAL_PROVIDER_DRIFT: 0.6,
            ReasonCode.WEBSOCKET_FLOOD_PATTERN: 0.7,
            ReasonCode.EDGE_ATTESTATION_FAILURE: 1.0,
            ReasonCode.GEO_ROUTING_IMPOSSIBLE: 0.8,
            ReasonCode.PRIVILEGE_ESCALATION_ATTEMPT: 1.0,
            ReasonCode.AUDIT_CHAIN_CORRUPTION: 1.0,
            ReasonCode.SYNCHRONIZATION_TAMPERING: 1.0
        }

    def evaluate_threat(self, signals: List[ReasonCode], staleness_seconds: float = 0.0) -> Dict[str, Any]:
        """
        Evaluates threat level deterministically.
        Applies confidence degradation if telemetry is stale.
        """
        if not signals:
            return {"detected": False, "score": 0.0}
            
        metrics_store.record_cyber_action("threat_signals_total", len(signals))
        
        # Calculate base score
        score = sum([self.signal_weights.get(sig, 0.0) for sig in signals])
        
        # Cap base score
        score = min(score, 1.0)
        
        # Confidence degradation based on stale telemetry
        confidence = 1.0
        degradation_reason = None
        if staleness_seconds > 300: # 5 minutes stale
            confidence = max(0.1, 1.0 - (staleness_seconds / 3600.0)) # linear degradation up to an hour
            degradation_reason = "telemetry_stale"
            score = score * confidence
            
        detected = score > 0.75
        
        # Generate deterministic reasoning hash
        reasoning_str = f"signals:{[s.value for s in signals]}|score:{score}|conf:{confidence}"
        reasoning_hash = hashlib.sha256(reasoning_str.encode()).hexdigest()
        
        result = {
            "detected": detected,
            "score": score,
            "confidence": confidence,
            "confidence_degradation_reason": degradation_reason,
            "reasoning_hash": reasoning_hash,
            "signals": [s.value for s in signals]
        }
        
        if detected:
            metrics_store.record_cyber_action("cyber_incidents_total")
            logger.warning(f"Threat detected deterministically: {result}")
            
        return result

detection_engine = CyberDetectionEngine()
