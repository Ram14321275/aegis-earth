from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.core.predictive.explainability.contracts import Explanation

class RemediationAction(BaseModel):
    action_type: str # e.g. "SCALE_WORKERS", "FLUSH_CACHE", "THROTTLE_API"
    target: str
    parameters: dict

class RecoveryWorkflow(BaseModel):
    workflow_id: str
    steps: List[RemediationAction]
    rollback_steps: List[RemediationAction]

class AutonomousDecision(BaseModel):
    decision_id: str
    timestamp: datetime
    trigger_source: str # e.g. "InfrastructureForecast"
    recommended_workflow: RecoveryWorkflow
    explainability: Explanation
    is_executed_automatically: bool
    status: str # "PENDING", "EXECUTED", "ROLLED_BACK"

class RemediationPlan(BaseModel):
    plan_id: str
    decisions: List[AutonomousDecision]
    overall_risk_reduction: str
