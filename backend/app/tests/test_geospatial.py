import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_search_location_valid():
    response = client.get("/api/v1/geospatial/search?query=San+Francisco")
    assert response.status_code == 200
    data = response.json().get("data", [])
    assert isinstance(data, list)
    assert len(data) > 0
    assert "Mocked Location for 'San Francisco'" in data[0]["name"]
    assert "coordinates" in data[0]

def test_search_location_invalid_query():
    # Query length < 2
    response = client.get("/api/v1/geospatial/search?query=a")
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"

def test_reverse_geocode_valid():
    response = client.get("/api/v1/geospatial/reverse?lat=37.7749&lon=-122.4194")
    assert response.status_code == 200
    data = response.json().get("data", {})
    assert "Mocked Place" in data["name"]
    assert data["country"] == "Mock Country"

def test_reverse_geocode_invalid_lat():
    # Lat > 90
    response = client.get("/api/v1/geospatial/reverse?lat=91.0&lon=-122.4194")
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"

def test_reverse_geocode_invalid_lon():
    # Lon < -180
    response = client.get("/api/v1/geospatial/reverse?lat=37.7749&lon=-181.0")
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"
