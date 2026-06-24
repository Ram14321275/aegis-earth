import pytest
import hmac
import hashlib
from app.core.cyber.attestation.verifier import attestation_verifier

def test_attestation_verification():
    secret = b"mock_master_secret"
    node_id = "edge_123"
    nonce = "abcd"
    
    message = f"{node_id}:{nonce}".encode()
    valid_sig = hmac.new(secret, message, hashlib.sha256).hexdigest()
    
    assert attestation_verifier.verify_attestation(node_id, nonce, valid_sig) is True
    assert attestation_verifier.verify_attestation(node_id, nonce, "invalid_sig") is False
