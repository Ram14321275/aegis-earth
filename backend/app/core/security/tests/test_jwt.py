import pytest
from datetime import timedelta
from app.core.security.jwt import create_token, decode_token

def test_create_and_decode_token():
    token = create_token("user123", "tenant456", "admin", timedelta(minutes=5))
    payload = decode_token(token)
    assert payload["sub"] == "user123"
    assert payload["tenant_id"] == "tenant456"
    assert payload["role"] == "admin"
