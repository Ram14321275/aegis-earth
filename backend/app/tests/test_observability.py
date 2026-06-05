import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.observability.metrics import metrics_store


def test_metrics_store():
    metrics_store.record_api_request(True, 150.0)
    metrics_store.record_api_request(False, 50.0)
    metrics_store.record_cache_access(True)
    metrics_store.record_cache_access(False)
    metrics_store.record_analysis("flood", 85.0)
    metrics_store.record_alerts_generated("CRITICAL")
    metrics_store.record_visualization_request()
    
    metrics = metrics_store.get_metrics()
    assert metrics.alerts.alerts_critical_total >= 1
    assert metrics.visualizations.requests_total >= 1
    
    assert metrics.api.total_requests >= 2
    assert metrics.api.successful_requests >= 1
    assert metrics.cache.cache_hits_total >= 1
    assert metrics.analysis.total_analyses >= 1
    assert "flood" in metrics.analysis.hazard_breakdown


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_health_endpoint():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/v1/system/health")
        assert response.status_code == 200
        data = response.json()["data"]
        assert "status" in data
        assert "components" in data
        assert "api" in data["components"]
        assert "cache" in data["components"]
        assert "database" in data["components"]
        assert "satellite" in data
        assert "gee" in data


@pytest.mark.anyio
async def test_metrics_endpoint():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/v1/system/metrics")
        assert response.status_code == 200
        data = response.json()["data"]
        assert "api" in data
        assert "cache" in data
        assert "analysis" in data
        assert "alerts" in data
