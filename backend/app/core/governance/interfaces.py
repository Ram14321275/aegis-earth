from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime

class SignatureProvider(ABC):
    @abstractmethod
    def sign_payload(self, payload: str) -> str:
        pass

    @abstractmethod
    def verify_signature(self, payload: str, signature: str) -> bool:
        pass

    @property
    @abstractmethod
    def algorithm_name(self) -> str:
        pass

class AuditProvider(ABC):
    @abstractmethod
    async def record_event(self, event_data: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    async def verify_chain(self, start_time: datetime, end_time: datetime) -> bool:
        pass

class ReplayProvider(ABC):
    @abstractmethod
    async def reconstruct_state(self, timestamp: datetime, tenant_id: str) -> Dict[str, Any]:
        pass

class GovernancePolicyProvider(ABC):
    @abstractmethod
    def evaluate_policy(self, policy_name: str, context: Dict[str, Any]) -> bool:
        pass

class SovereigntyResolver(ABC):
    @abstractmethod
    def is_export_allowed(self, tenant_id: str, target_region: str) -> bool:
        pass
