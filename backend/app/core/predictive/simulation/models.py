from pydantic import BaseModel
from typing import List
from datetime import datetime
from app.core.predictive.explainability.contracts import Explanation

class RegionalImpactProjection(BaseModel):
    region_id: str
    impacted_population: int
    infrastructure_damage_estimate: str
    projected_severity: float

class CascadeProjection(BaseModel):
    cascade_id: str
    trigger_hazard: str
    resultant_hazards: List[str]
    timeline_offset_hours: int

class EnvironmentalTrajectory(BaseModel):
    trajectory_id: str
    parameters: dict

class ScenarioSimulation(BaseModel):
    simulation_id: str
    tenant_id: str
    scenario_name: str
    executed_at: datetime
    horizon_hours: int
    regional_impacts: List[RegionalImpactProjection]
    cascades: List[CascadeProjection]
    trajectories: List[EnvironmentalTrajectory]
    explainability: Explanation
