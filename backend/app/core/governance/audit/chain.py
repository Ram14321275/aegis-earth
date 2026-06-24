from typing import Dict, Any, List, Optional
import logging

from app.core.governance.audit.hashing import generate_chained_hash

logger = logging.getLogger(__name__)

class AuditChainValidator:
    @staticmethod
    def verify_chain(events: List[Dict[str, Any]]) -> bool:
        """
        Verifies the cryptographic integrity of a sequence of audit events.
        Events must be sorted by sequence number.
        """
        if not events:
            return True

        expected_sequence = events[0].get("immutable_sequence_number", 0)

        for i, event in enumerate(events):
            # Check sequence numbers
            seq = event.get("immutable_sequence_number")
            if seq != expected_sequence:
                logger.error(f"Chain broken at sequence {seq}. Expected {expected_sequence}.")
                return False
            expected_sequence += 1

            # Check chained hashes
            if i > 0:
                parent_event = events[i - 1]
                expected_parent_hash = parent_event.get("payload_hash")
                current_parent_hash = event.get("parent_hash")
                
                if current_parent_hash != expected_parent_hash:
                    logger.error(f"Hash mismatch at event {event.get('event_id')}.")
                    return False

        return True
