from typing import Any, Dict
from abc import ABC, abstractmethod
from app.core.fusion.models import ReliabilityAssessment, RegionalThreatAssessment

class MLConfidenceCalibrationInterface(ABC):
    """
    Future boundary for ML-driven confidence calibration.
    """
    @abstractmethod
    async def calibrate(self, raw_assessment: Dict[str, Any]) -> ReliabilityAssessment:
        pass

class AnomalyPredictionInterface(ABC):
    """
    Future boundary for ML-driven anomaly prediction.
    """
    @abstractmethod
    async def predict_anomalies(self, history: list[Dict[str, Any]]) -> list[Dict[str, Any]]:
        pass

class EvacuationSimulationInterface(ABC):
    """
    Future boundary for ML-driven evacuation routing and simulation.
    """
    @abstractmethod
    async def simulate_evacuation(self, threat_assessment: RegionalThreatAssessment) -> Dict[str, Any]:
        pass

class ForecastingModelInterface(ABC):
    """
    Future boundary for global disaster forecasting.
    """
    @abstractmethod
    async def forecast_disaster(self, region_id: str, days_ahead: int) -> Dict[str, Any]:
        pass
