import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.alert import Alert
from app.db.models.analysis import Analysis
from app.db.models.audit import AuditLog
from app.db.models.location import Location
from app.db.models.risk import RiskAssessment
from app.db.repositories.alert_repository import alert_repo
from app.db.repositories.analysis_repository import analysis_repo
from app.db.repositories.audit_repository import audit_repo
from app.db.repositories.location_repository import location_repo
from app.db.repositories.risk_repository import risk_repo
from app.observability.metrics import metrics_store


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def db_session():
    from unittest.mock import AsyncMock, MagicMock
    session_mock = AsyncMock()
    session_mock.add = MagicMock()
    
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    
    async def mock_refresh(obj):
        obj.id = "mock-id"
        
    session_mock.refresh = mock_refresh
    class MockObj:
        def __init__(self, **kwargs):
            self.id = "mock-id"
            for k, v in kwargs.items():
                setattr(self, k, v)
                
    def mock_first():
        return MockObj(city="Test City")
        
    def mock_all():
        return [MockObj(city="Test City")]
        
    mock_scalars.first = mock_first
    mock_scalars.all = mock_all
    mock_result.scalars.return_value = mock_scalars
    session_mock.execute.return_value = mock_result
    
    return session_mock


@pytest.mark.anyio
async def test_location_repository(db_session: AsyncSession):
    # Test Create
    loc_data = {
        "city": "Test City",
        "state_province": "TS",
        "country": "Test Country",
        "latitude": 10.0,
        "longitude": 20.0,
        "query": "Test City",
    }
    loc = await location_repo.create(db_session, obj_in=loc_data)
    assert loc.id is not None
    assert loc.city == "Test City"

    # Test Get
    retrieved = await location_repo.get(db_session, loc.id)
    assert retrieved is not None
    assert retrieved.city == "Test City"

    # Test Get Multi
    multi = await location_repo.get_multi(db_session)
    assert len(multi) >= 1

    # Test Metrics
    metrics = metrics_store.get_metrics()
    assert metrics.database.queries_total > 0


@pytest.mark.anyio
async def test_analysis_repository(db_session: AsyncSession):
    loc_data = {
        "city": "Test City",
        "state_province": "TS",
        "country": "Test Country",
        "latitude": 10.0,
        "longitude": 20.0,
        "query": "Test City",
    }
    loc = await location_repo.create(db_session, obj_in=loc_data)

    analysis_data = {
        "location_id": loc.id,
        "hazard_type": "flood",
        "analysis_version": "1.0",
        "source": "test",
    }
    analysis = await analysis_repo.create(db_session, obj_in=analysis_data)
    assert analysis.id is not None
    assert analysis.location_id == loc.id


@pytest.mark.anyio
async def test_risk_and_alert_repository(db_session: AsyncSession):
    loc_data = {
        "city": "Test City",
        "state_province": "TS",
        "country": "Test Country",
        "latitude": 10.0,
        "longitude": 20.0,
        "query": "Test City",
    }
    loc = await location_repo.create(db_session, obj_in=loc_data)

    analysis_data = {
        "location_id": loc.id,
        "hazard_type": "flood",
        "analysis_version": "1.0",
        "source": "test",
    }
    analysis = await analysis_repo.create(db_session, obj_in=analysis_data)

    risk_data = {
        "analysis_id": analysis.id,
        "risk_score": 85.0,
        "risk_level": "HIGH",
        "confidence": 0.9,
    }
    risk = await risk_repo.create(db_session, obj_in=risk_data)
    assert risk.risk_level == "HIGH"

    alert_data = {
        "analysis_id": analysis.id,
        "severity": "CRITICAL",
        "title": "Flood Warning",
        "message": "Critical flooding expected.",
    }
    alert = await alert_repo.create(db_session, obj_in=alert_data)
    assert alert.severity == "CRITICAL"


@pytest.mark.anyio
async def test_audit_repository(db_session: AsyncSession):
    audit_data = {
        "action": "CREATE",
        "entity_type": "Location",
        "entity_id": "test-id",
        "details": {"test": "data"},
    }
    audit = await audit_repo.create(db_session, obj_in=audit_data)
    assert audit.action == "CREATE"
    assert audit.details["test"] == "data"
