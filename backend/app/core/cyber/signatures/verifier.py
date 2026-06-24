from typing import Any
import hmac
import hashlib

class SignatureVerifier:
    """Cryptographic signature validation."""
    
    @staticmethod
    def verify_hmac(secret: bytes, payload: bytes, signature: str) -> bool:
        expected = hmac.new(secret, payload, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)
