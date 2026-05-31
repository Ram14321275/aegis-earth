from datetime import datetime, timezone

from app.schemas.intelligence import DisasterSignal, IntelligenceResponse, ResolvedLocation, RiskBand
from app.services.alert_engine.alerts import generate_alerts
from app.services.visualization.layers import build_evidence_layers


class DisasterEngine:
    def analyze(self, location: ResolvedLocation) -> IntelligenceResponse:
        signals = self._score_signals(location)
        overall_risk = self._overall_risk(signals)
        confidence = round(sum(signal.confidence for signal in signals) / len(signals), 2)

        return IntelligenceResponse(
            location_name=location.location_name,
            coordinates=location.coordinates,
            generated_at=datetime.now(timezone.utc),
            overall_risk=overall_risk,
            confidence=confidence,
            signals=signals,
            evidence_layers=build_evidence_layers(),
            alerts=generate_alerts(signals),
            explanation=[
                "Flood risk is scored from rainfall sensitivity, drainage exposure, and urban surface assumptions.",
                "Wildfire risk is scored from surface heat sensitivity, vegetation dryness assumptions, and wind exposure.",
                "Sprint 1 uses deterministic explainable rules while model-interface remains ready for replaceable AI models.",
            ],
        )

    def _score_signals(self, location: ResolvedLocation) -> list[DisasterSignal]:
        latitude_factor = abs(location.coordinates.latitude) / 90
        longitude_factor = abs(location.coordinates.longitude) / 180
        urban_demo_boost = 0.14 if location.source == "city" else 0.08

        flood_confidence = min(0.91, 0.66 + urban_demo_boost + longitude_factor * 0.08)
        wildfire_confidence = min(0.86, 0.55 + latitude_factor * 0.16)

        return [
            DisasterSignal(
                type="flood",
                risk=self._band(flood_confidence),
                confidence=round(flood_confidence, 2),
                drivers=[
                    "Rainfall anomaly sensitivity",
                    "Low-lying catchment exposure",
                    "Impervious surface runoff potential",
                ],
            ),
            DisasterSignal(
                type="wildfire",
                risk=self._band(wildfire_confidence),
                confidence=round(wildfire_confidence, 2),
                drivers=[
                    "Surface temperature sensitivity",
                    "Vegetation dryness proxy",
                    "Wind exposure placeholder",
                ],
            ),
        ]

    def _band(self, score: float) -> RiskBand:
        if score >= 0.88:
            return "critical"
        if score >= 0.74:
            return "high"
        if score >= 0.58:
            return "moderate"
        return "low"

    def _overall_risk(self, signals: list[DisasterSignal]) -> RiskBand:
        priority: dict[RiskBand, int] = {"low": 0, "moderate": 1, "high": 2, "critical": 3}
        return max((signal.risk for signal in signals), key=lambda risk: priority[risk])

