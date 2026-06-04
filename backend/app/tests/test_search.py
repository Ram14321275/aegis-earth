import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_search_request_validation():
    # Only query
    response = client.post("/api/v1/search", json={"query": "Hyderabad"})
    assert response.status_code == 200
    
    # Only coords
    response = client.post("/api/v1/search", json={"latitude": 17.385, "longitude": 78.4867})
    assert response.status_code == 200

    # Both -> Reject
    response = client.post("/api/v1/search", json={"query": "Hyderabad", "latitude": 17.385, "longitude": 78.4867})
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"

    # Neither -> Reject
    response = client.post("/api/v1/search", json={})
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"
    
    # Partial coords -> Reject
    response = client.post("/api/v1/search", json={"latitude": 17.385})
    assert response.status_code == 422

def test_search_endpoint_returns_analysis_result():
    response = client.post("/api/v1/search", json={"query": "Hyderabad"})
    assert response.status_code == 200
    
    data = response.json().get("data", {})
    assert "risk_assessment" in data
    assert "visualizations" in data
    assert "location_name" in data
    assert "coordinates" in data
    assert data["risk_assessment"]["hazard_type"] == "flood"
    assert "cache_hit" in data["metadata"]

def test_search_endpoint_cache_hit():
    from unittest.mock import AsyncMock, patch

    city = "CacheTestCity"
    
    with patch("app.services.search.service.cache_manager.get_or_fetch", new_callable=AsyncMock) as mock_get_or_fetch:
        # First request - Cache Miss (simulate hit=False)
        # return an AnalysisResult but since the function returns AnalysisResult and bool we can mock its return
        from app.schemas.intelligence import AnalysisResult, RiskAssessment
        from app.schemas.geospatial import Coordinates
        
        dummy_result = AnalysisResult(
            location_name=city,
            coordinates=Coordinates(lat=0.0, lon=0.0),
            risk_assessment=RiskAssessment(
                hazard_type="flood", 
                overall_score=0.0, 
                severity_level="LOW",
                source=["mock"],
                confidence=1.0,
                severity="low",
                analysis_version="1.0",
                score=0.0
            ),
            source=["mock"],
            confidence=1.0,
            severity="low",
            analysis_version="1.0",
            metadata={}
        )
        
        mock_get_or_fetch.side_effect = [
            (dummy_result, False),  # First call miss
            (dummy_result, True)    # Second call hit
        ]

        response1 = client.post("/api/v1/search", json={"query": city})
        assert response1.status_code == 200
        assert response1.json()["data"]["metadata"]["cache_hit"] is False
        
        response2 = client.post("/api/v1/search", json={"query": city})
        assert response2.status_code == 200
        assert response2.json()["data"]["metadata"]["cache_hit"] is True
