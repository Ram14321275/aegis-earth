from pydantic import BaseModel
from typing import Optional, List

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: Optional[str] = None

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    tenant_id: Optional[str] = None
    role: Optional[str] = None

class UserCreate(BaseModel):
    email: str
    password: str
    role: Optional[str] = "viewer"

class UserResponse(BaseModel):
    id: str
    email: str
    role: str
    tenant_id: str
    is_active: bool

class APIKeyCreate(BaseModel):
    name: str
    scopes: List[str]

class APIKeyResponse(BaseModel):
    id: str
    name: str
    prefix: str
    scopes: List[str]
    api_key: Optional[str] = None # Only returned on creation
