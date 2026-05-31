from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_api_v1_health() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "status": "healthy",
            "service": "Aegis Earth",
            "version": "v1",
        },
        "error": None
    }
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"

