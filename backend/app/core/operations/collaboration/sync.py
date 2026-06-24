import asyncio
from typing import Dict, List, Set, Any
from datetime import datetime, timezone

from app.observability.metrics import metrics_store

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class CollaborationSyncEngine:
    def __init__(self):
        # tenant_id -> room_id -> set of active operators
        self.rooms: Dict[str, Dict[str, Set[str]]] = {}
        # tenant_id -> room_id -> dict of operator states (e.g. cursors)
        self.operator_states: Dict[str, Dict[str, Dict[str, Any]]] = {}
        
    async def join_room(self, tenant_id: str, room_id: str, operator_id: str):
        if tenant_id not in self.rooms:
            self.rooms[tenant_id] = {}
        if room_id not in self.rooms[tenant_id]:
            self.rooms[tenant_id][room_id] = set()
            
        self.rooms[tenant_id][room_id].add(operator_id)
        metrics_store.record_command_center_action("operator_presence_count", 1)

    async def leave_room(self, tenant_id: str, room_id: str, operator_id: str):
        if tenant_id in self.rooms and room_id in self.rooms[tenant_id]:
            if operator_id in self.rooms[tenant_id][room_id]:
                self.rooms[tenant_id][room_id].remove(operator_id)
                metrics_store.record_command_center_action("operator_presence_count", -1)
                
            if tenant_id in self.operator_states and room_id in self.operator_states[tenant_id]:
                if operator_id in self.operator_states[tenant_id][room_id]:
                    del self.operator_states[tenant_id][room_id][operator_id]

    async def update_state(self, tenant_id: str, room_id: str, operator_id: str, state: dict):
        if tenant_id not in self.operator_states:
            self.operator_states[tenant_id] = {}
        if room_id not in self.operator_states[tenant_id]:
            self.operator_states[tenant_id][room_id] = {}
            
        # Optimistic concurrency: apply state payload
        self.operator_states[tenant_id][room_id][operator_id] = {
            "state": state,
            "last_updated": utc_now().isoformat()
        }

    def get_room_state(self, tenant_id: str, room_id: str) -> dict:
        states = self.operator_states.get(tenant_id, {}).get(room_id, {})
        active = list(self.rooms.get(tenant_id, {}).get(room_id, set()))
        return {
            "active_operators": active,
            "states": states
        }
