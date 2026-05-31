from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

RiskBand = Literal["low", "moderate", "high", "critical"]


class Coordinates(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class AnalysisRequest(BaseModel):
    query: str = Field(min_length=2, max_length=160)


class ResolvedLocation(BaseModel):
    location_name: str
    coordinates: Coordinates
    source: Literal["city", "coordinates"]


class DisasterSignal(BaseModel):
    type: Literal["flood", "wildfire"]
    risk: RiskBand
    confidence: float = Field(ge=0, le=1)
    drivers: list[str]


class EvidenceLayer(BaseModel):
    id: str
    label: str
    type: Literal["map", "heatmap", "difference"]
    description: str


class AlertItem(BaseModel):
    id: str
    severity: RiskBand
    title: str
    message: str


class IntelligenceResponse(BaseModel):
    location_name: str = Field(serialization_alias="locationName")
    coordinates: Coordinates
    generated_at: datetime = Field(serialization_alias="generatedAt")
    overall_risk: RiskBand = Field(serialization_alias="overallRisk")
    confidence: float = Field(ge=0, le=1)
    signals: list[DisasterSignal]
    evidence_layers: list[EvidenceLayer] = Field(serialization_alias="evidenceLayers")
    alerts: list[AlertItem]
    explanation: list[str]

