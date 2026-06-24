from typing import Dict, Any, Optional
from datetime import datetime, timezone
from app.core.integrations.normalization.models import CanonicalHazardEvent, NormalizedSeverity
from app.observability.metrics import metrics_store
import logging

logger = logging.getLogger(__name__)

class NormalizationEngine:
    VERSION = "v1.0"

    def normalize(self, provider_id: str, event_id: str, payload: Dict[str, Any]) -> Optional[CanonicalHazardEvent]:
        """
        Deterministically normalizes an external payload into the Aegis Earth Canonical Format.
        This isolates all internal orchestration from external schemas.
        """
        try:
            # Simulated provider-specific mapping
            # In a real system, we'd lookup a normalization adapter based on provider_id
            
            canonical_type = str(payload.get("type", "UNKNOWN")).upper()
            
            # Timestamp reconciliation
            ts_str = payload.get("time") or payload.get("timestamp")
            if ts_str:
                try:
                    dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                except ValueError:
                    dt = datetime.now(timezone.utc)
            else:
                dt = datetime.now(timezone.utc)

            # Severity normalization
            raw_severity = str(payload.get("severity", "info")).lower()
            if raw_severity in ["extreme", "critical", "severe"]:
                sev = NormalizedSeverity(level="CRITICAL", score=0.9)
            elif raw_severity in ["high", "major"]:
                sev = NormalizedSeverity(level="HIGH", score=0.7)
            elif raw_severity in ["moderate", "warning"]:
                sev = NormalizedSeverity(level="WARNING", score=0.4)
            else:
                sev = NormalizedSeverity(level="INFO", score=0.1)

            # Confidence adjustments
            provider_confidence = float(payload.get("confidence", 0.5))
            adjusted_confidence = min(1.0, max(0.0, provider_confidence * 0.9)) # slight penalty for external unverified

            coords = payload.get("coordinates", {})
            lat = float(coords.get("lat", 0.0))
            lon = float(coords.get("lon", 0.0))

            event = CanonicalHazardEvent(
                event_type=canonical_type,
                timestamp=dt,
                latitude=lat,
                longitude=lon,
                severity=sev,
                confidence=adjusted_confidence,
                provider_source=provider_id,
                original_event_id=event_id,
                metadata={"normalization_version": self.VERSION}
            )
            return event
        except Exception as e:
            metrics_store.record_command_center_action("normalization_failures_total")
            logger.error(f"Normalization failed for {provider_id} event {event_id}: {e}")
            return None

normalization_engine = NormalizationEngine()
