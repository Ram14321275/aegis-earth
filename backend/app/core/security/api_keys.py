import hashlib
import secrets
from typing import Tuple

def generate_api_key() -> Tuple[str, str, str]:
    """
    Generates a secure API key.
    Returns:
        Tuple of (raw_key, key_hash, prefix)
    """
    prefix = secrets.token_urlsafe(8)
    body = secrets.token_urlsafe(32)
    raw_key = f"aegis_{prefix}_{body}"
    key_hash = hash_api_key(raw_key)
    return raw_key, key_hash, prefix

def hash_api_key(raw_key: str) -> str:
    """
    Hashes an API key for storage.
    """
    return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()
