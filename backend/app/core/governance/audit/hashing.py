import json
import hashlib
from typing import Any, Dict

def generate_deterministic_hash(data: Dict[str, Any]) -> str:
    """
    Generates a deterministic SHA-256 hash of a dictionary by sorting keys.
    """
    serialized = json.dumps(data, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(serialized.encode('utf-8')).hexdigest()

def generate_chained_hash(parent_hash: str, payload_hash: str) -> str:
    """
    Generates a chained hash based on parent and current payload.
    """
    combined = f"{parent_hash}::{payload_hash}"
    return hashlib.sha256(combined.encode('utf-8')).hexdigest()
