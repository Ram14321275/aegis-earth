# Placeholder for SQLAlchemy Models or equivalent
# Requires tenant-aware, immutable lineage, PostGIS support, explainability payload storage.

from typing import Any

class PredictiveRecordModel:
    """
    Base model for predictive records.
    Ensures tenant_id and explainability payloads are stored.
    """
    pass

class ForecastRecord(PredictiveRecordModel):
    pass

class RemediationRecord(PredictiveRecordModel):
    pass

class AnomalyRecord(PredictiveRecordModel):
    pass

class SimulationRecord(PredictiveRecordModel):
    pass
