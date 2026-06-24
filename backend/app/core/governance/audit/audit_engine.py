import uuid
from typing import Dict, Any, Optional
from datetime import datetime, timezone
import logging

from app.core.governance.interfaces import AuditProvider, SignatureProvider
from app.core.governance.audit.hashing import generate_deterministic_hash, generate_chained_hash
from app.core.governance.audit.lineage import LineageBuilder
from app.observability.metrics import metrics_store

logger = logging.getLogger(__name__)

class ImmutableAuditEngine(AuditProvider):
    def __init__(self, signature_provider: SignatureProvider):
        self.signature_provider = signature_provider
        # Mocking an in-memory store for sequence and parent tracking since DB is async
        self._current_sequence: int = 1
        self._last_event_hash: Optional[str] = None

    async def record_event(
        self, 
        tenant_id: str, 
        actor_id: str, 
        action_type: str, 
        payload: Dict[str, Any],
        request_data: Optional[Dict[str, Any]] = None,
        reasoning_data: Optional[Dict[str, Any]] = None,
        parent_event_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        parent_lineage: str = ""
    ) -> Dict[str, Any]:
        """
        Records an immutable audit event with cryptographic tamper detection.
        """
        metrics_store.record_governance_action("audit_events_total")
        
        event_id = f"aud-{uuid.uuid4()}"
        timestamp = datetime.now(timezone.utc).isoformat()
        
        payload_hash = generate_deterministic_hash(payload)
        request_hash = generate_deterministic_hash(request_data) if request_data else None
        reasoning_hash = generate_deterministic_hash(reasoning_data) if reasoning_data else None
        
        lineage_path = LineageBuilder.build_path(parent_lineage, event_id)
        
        # Build event record
        event_record = {
            "event_id": event_id,
            "tenant_id": tenant_id,
            "actor_id": actor_id,
            "action_type": action_type,
            "timestamp": timestamp,
            "request_hash": request_hash,
            "payload_hash": payload_hash,
            "reasoning_hash": reasoning_hash,
            "parent_event_id": parent_event_id,
            "correlation_id": correlation_id,
            "lineage_path": lineage_path,
            "immutable_sequence_number": self._current_sequence,
            "parent_hash": self._last_event_hash, # Used for chaining
            "signature_algorithm": self.signature_provider.algorithm_name,
            "signature_version": "v1",
            "key_version": getattr(self.signature_provider, "key_version", "v1")
        }

        # Generate Signature
        signature = self.signature_provider.sign_payload(generate_deterministic_hash(event_record))
        event_record["signature"] = signature
        
        # Update chain state
        self._last_event_hash = payload_hash
        self._current_sequence += 1
        
        logger.info(f"Recorded immutable audit event: {event_id} for action {action_type}")
        return event_record

    async def verify_chain(self, start_time: datetime, end_time: datetime) -> bool:
        # In a real implementation, this would fetch events from the DB
        # and use AuditChainValidator.verify_chain(events)
        pass

# Initialize a default instance for DI
from app.core.governance.audit.signatures import HMACSHA256Provider
import os

default_secret = os.getenv("AEGIS_GOVERNANCE_SECRET", "default_insecure_secret_for_dev")
audit_engine = ImmutableAuditEngine(HMACSHA256Provider(secret_key=default_secret))
