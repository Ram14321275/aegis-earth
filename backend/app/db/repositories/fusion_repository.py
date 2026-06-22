from app.db.repositories.base_repository import BaseRepository
from app.db.models.fusion import (
    FusedRegionalAssessment,
    CorrelationEvent,
    ReliabilitySnapshot,
    EscalationEvent,
    AnomalyRecord
)

class FusedRegionalAssessmentRepository(BaseRepository[FusedRegionalAssessment]):
    def __init__(self):
        super().__init__(FusedRegionalAssessment)

class CorrelationEventRepository(BaseRepository[CorrelationEvent]):
    def __init__(self):
        super().__init__(CorrelationEvent)

class ReliabilitySnapshotRepository(BaseRepository[ReliabilitySnapshot]):
    def __init__(self):
        super().__init__(ReliabilitySnapshot)

class EscalationEventRepository(BaseRepository[EscalationEvent]):
    def __init__(self):
        super().__init__(EscalationEvent)

class AnomalyRecordRepository(BaseRepository[AnomalyRecord]):
    def __init__(self):
        super().__init__(AnomalyRecord)

fused_regional_assessment_repository = FusedRegionalAssessmentRepository()
correlation_event_repository = CorrelationEventRepository()
reliability_snapshot_repository = ReliabilitySnapshotRepository()
escalation_event_repository = EscalationEventRepository()
anomaly_record_repository = AnomalyRecordRepository()
