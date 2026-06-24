import hmac
import hashlib
from app.core.governance.interfaces import SignatureProvider

class HMACSHA256Provider(SignatureProvider):
    def __init__(self, secret_key: str, key_version: str = "v1"):
        self.secret_key = secret_key
        self.key_version = key_version

    def sign_payload(self, payload: str) -> str:
        return hmac.new(
            self.secret_key.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def verify_signature(self, payload: str, signature: str) -> bool:
        expected = self.sign_payload(payload)
        return hmac.compare_digest(expected, signature)

    @property
    def algorithm_name(self) -> str:
        return "HMAC-SHA256"
