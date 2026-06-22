import os
import jwt
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

# Asymmetric readiness: We default to symmetric (HS256) but allow RS256 if keys are provided.
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
PRIVATE_KEY = os.getenv("JWT_PRIVATE_KEY")
PUBLIC_KEY = os.getenv("JWT_PUBLIC_KEY")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", "10080")) # 7 days

def get_signing_key():
    if ALGORITHM.startswith("RS") and PRIVATE_KEY:
        return PRIVATE_KEY
    return SECRET_KEY

def get_verifying_key():
    if ALGORITHM.startswith("RS") and PUBLIC_KEY:
        return PUBLIC_KEY
    return SECRET_KEY

def create_token(subject: str, tenant_id: str, role: str, expires_delta: timedelta, token_type: str = "access") -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {
        "exp": expire,
        "sub": subject,
        "tenant_id": tenant_id,
        "role": role,
        "type": token_type,
        "iat": datetime.now(timezone.utc)
    }
    encoded_jwt = jwt.encode(to_encode, get_signing_key(), algorithm=ALGORITHM)
    return encoded_jwt

def create_access_token(subject: str, tenant_id: str, role: str) -> str:
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_token(subject, tenant_id, role, expires_delta, token_type="access")

def create_refresh_token(subject: str, tenant_id: str, role: str) -> str:
    expires_delta = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    return create_token(subject, tenant_id, role, expires_delta, token_type="refresh")

def decode_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, get_verifying_key(), algorithms=[ALGORITHM])
