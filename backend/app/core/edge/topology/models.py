from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

class EdgeNodeConfig(BaseModel):
    node_id: str
    sovereign_region: str
    jurisdiction: str
    latency_profile: str = "high-bandwidth"

class EdgeNodeState(BaseModel):
    node_id: str
    health_state: str = "ACTIVE" # ACTIVE, DEGRADED, OFFLINE
    synchronization_state: str = "IN_SYNC"
    replay_checkpoint: Optional[str] = None
    shard_assignments: List[str] = Field(default_factory=list)
    governance_signature: Optional[str] = None
    last_heartbeat: datetime
