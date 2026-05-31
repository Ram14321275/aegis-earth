from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_analyze_coordinates() -> None:
    response = client.post("/api/v1/intelligence/analyze", json={"query": "17.3850,78.4867"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["coordinates"]["latitude"] == 17.385
    assert payload["overallRisk"] in {"low", "moderate", "high", "critical"}
    assert len(payload["signals"]) == 2

