import secrets
from typing import Dict
from datetime import datetime, timedelta, timezone

from app.core.security.jwt import create_token, decode_token

def generate_streaming_ticket(subject: str, tenant_id: str, role: str) -> str:
    """
    Generates a very short-lived ticket (e.g. 1 minute) used specifically 
    for authenticating a new WebSocket connection.
    """
    expires_delta = timedelta(minutes=1)
    return create_token(
        subject=subject,
        tenant_id=tenant_id,
        role=role,
        expires_delta=expires_delta,
        token_type="streaming_ticket"
    )

def validate_streaming_ticket(ticket: str) -> Dict:
    """
    Validates the ticket. Raises Exception if invalid or expired.
    """
    payload = decode_token(ticket)
    if payload.get("type") != "streaming_ticket":
        raise ValueError("Invalid token type for streaming")
    return payload
