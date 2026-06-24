import pytest
import time
import hmac
import hashlib
from app.core.integrations.webhooks.security import WebhookSecurity

def test_webhook_signature_verification():
    secret = "test_secret"
    payload = b'{"event":"test"}'
    
    timestamp = str(int(time.time()))
    signed_payload = f"{timestamp}.{payload.decode('utf-8')}".encode("utf-8")
    signature = hmac.new(
        secret.encode("utf-8"),
        signed_payload,
        hashlib.sha256
    ).hexdigest()
    
    signature_header = f"t={timestamp},v1={signature}"
    
    assert WebhookSecurity.verify_signature(payload, signature_header, secret) is True
    
    # Invalid signature
    invalid_header = f"t={timestamp},v1=invalidsig"
    assert WebhookSecurity.verify_signature(payload, invalid_header, secret) is False
    
    # Timestamp drift (replay attack prevention)
    old_timestamp = str(int(time.time()) - 400) # > 300 seconds (5 min limit)
    old_signed_payload = f"{old_timestamp}.{payload.decode('utf-8')}".encode("utf-8")
    old_signature = hmac.new(
        secret.encode("utf-8"),
        old_signed_payload,
        hashlib.sha256
    ).hexdigest()
    
    old_header = f"t={old_timestamp},v1={old_signature}"
    assert WebhookSecurity.verify_signature(payload, old_header, secret) is False
