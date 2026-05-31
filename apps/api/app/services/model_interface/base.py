from abc import ABC, abstractmethod

from app.schemas.intelligence import ResolvedLocation, DisasterSignal


class DisasterModel(ABC):
    @abstractmethod
    def infer(self, location: ResolvedLocation) -> list[DisasterSignal]:
        """Return explainable disaster signals for a resolved location."""

