import hmac
import hashlib
from typing import Optional
import time

class WebhookSecurity:
    MAX_TIMESTAMP_DRIFT_SECONDS = 300 # 5 minutes

    @staticmethod
    def verify_signature(payload: bytes, signature_header: str, secret: str) -> bool:
        """
        Verifies HMAC SHA-256 signature for inbound webhooks.
        Expected format: `t=<timestamp>,v1=<signature>` (similar to Stripe/GitHub)
        """
        try:
            parts = dict(part.split("=") for part in signature_header.split(","))
            timestamp = parts.get("t")
            signature = parts.get("v1")

            if not timestamp or not signature:
                return False

            # Check timestamp drift to prevent replay attacks
            if abs(time.time() - int(timestamp)) > WebhookSecurity.MAX_TIMESTAMP_DRIFT_SECONDS:
                return False

            # Compute expected signature
            signed_payload = f"{timestamp}.{payload.decode('utf-8')}".encode("utf-8")
            expected_signature = hmac.new(
                secret.encode("utf-8"),
                signed_payload,
                hashlib.sha256
            ).hexdigest()

            return hmac.compare_digest(expected_signature, signature)
        except Exception:
            return False
