import pytest
from app.core.security.api_keys import generate_api_key, hash_api_key

def test_generate_api_key():
    raw_key, key_hash, prefix = generate_api_key()
    assert raw_key.startswith(f"aegis_{prefix}_")
    assert key_hash == hash_api_key(raw_key)
