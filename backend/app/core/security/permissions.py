from enum import Enum

class SystemPermission(str, Enum):
    # Base
    READ_INTELLIGENCE = "intelligence:read"
    WRITE_INTELLIGENCE = "intelligence:write"
    
    # Streaming
    SUBSCRIBE_ALERTS = "streaming:alerts"
    SUBSCRIBE_EVENTS = "streaming:events"
    
    # Workers
    EXECUTE_JOBS = "jobs:execute"
    UPDATE_RISK = "risk:update"
    
    # Admin
    MANAGE_TENANT = "tenant:manage"
    MANAGE_USERS = "users:manage"
    MANAGE_API_KEYS = "api_keys:manage"
