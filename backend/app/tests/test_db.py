import pytest
from unittest.mock import AsyncMock, MagicMock

from app.db.models.analysis_record import AnalysisRecord
from app.db.models.location_search import LocationSearch
from app.db.repositories.analysis import AnalysisRepository
from app.db.repositories.location import LocationRepository

@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_location_repository_create():
    session_mock = AsyncMock()
    session_mock.add = MagicMock()
    repo = LocationRepository(session_mock)

    obj_in = {"query": "Hyderabad"}

    result = await repo.create(obj_in)

    assert isinstance(result, LocationSearch)
    assert result.query == "Hyderabad"
    session_mock.add.assert_called_once()
    session_mock.flush.assert_awaited_once()
    session_mock.refresh.assert_awaited_once_with(result)


@pytest.mark.anyio
async def test_location_repository_get_by_id():
    session_mock = AsyncMock()
    repo = LocationRepository(session_mock)

    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_location = LocationSearch(id="123", query="Hyderabad")
    mock_scalars.first.return_value = mock_location
    mock_result.scalars.return_value = mock_scalars
    session_mock.execute.return_value = mock_result

    result = await repo.get_by_id("123")

    assert result is not None
    assert result.id == "123"
    assert result.query == "Hyderabad"
    session_mock.execute.assert_awaited_once()


@pytest.mark.anyio
async def test_analysis_repository_create():
    session_mock = AsyncMock()
    session_mock.add = MagicMock()
    repo = AnalysisRepository(session_mock)

    obj_in = {
        "location_id": "123",
        "hazard_type": "flood",
        "risk_score": 85.5,
        "severity": "high",
        "analysis_version": "v1.0",
        "source": "mock",
    }

    result = await repo.create(obj_in)

    assert isinstance(result, AnalysisRecord)
    assert result.hazard_type == "flood"
    session_mock.add.assert_called_once()
    session_mock.flush.assert_awaited_once()
    session_mock.refresh.assert_awaited_once_with(result)
