from abc import ABC, abstractmethod
from typing import List

from app.core.intelligence.models import (
    IntelligenceSignal, CorrelatedHazard, IntelligenceExplanation, ForecastWindow
)


class AIProvider(ABC):
    """
    Abstract interface for AI/LLM providers (OpenAI, Gemini, Local).
    Ensures Aegis Earth is not tightly coupled to any single vendor.
    """
    
    @abstractmethod
    async def generate_explanation(
        self, 
        signals: List[IntelligenceSignal], 
        correlations: List[CorrelatedHazard]
    ) -> IntelligenceExplanation:
        """
        Generates human-readable reasoning and explanations based on detected signals and correlations.
        Implementation MUST NEVER leak provider secrets or expose prompt payloads directly.
        """
        pass


class ForecastingModel(ABC):
    """
    Future-ready interface for Anomaly Detection, ML pipelines, and Time-Series Forecasting models.
    """
    
    @abstractmethod
    async def forecast(self, signals: List[IntelligenceSignal]) -> List[ForecastWindow]:
        """
        Projects current intelligence signals into future risk anomaly windows.
        """
        pass
