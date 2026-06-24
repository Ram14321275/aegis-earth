from abc import ABC, abstractmethod
from typing import List
from app.core.copilot.models import ThreatSummary, CopilotRecommendation

class RecommendationEngineInterface(ABC):
    """Abstract interface for Recommendation Generation."""

    @abstractmethod
    def generate_recommendations(self, threats: List[ThreatSummary]) -> List[CopilotRecommendation]:
        pass
