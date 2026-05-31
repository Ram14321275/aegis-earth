import pytest

from app.core.visualization.service import visualization_service


def test_visualization_generation():
    result = visualization_service.generate_visualizations(
        lat=17.385, lon=78.4867, risk_level="HIGH", hazard_type="flood"
    )

    assert "heatmap" in result
    assert result["heatmap"].layer_id == "heatmap-01"
    assert len(result["heatmap"].points) == 1
    assert result["heatmap"].points[0].lat == 17.385

    assert "overlay" in result
    assert result["overlay"].layer_id == "risk-overlay"
    assert result["overlay"].color == "#FF0000"
    assert len(result["overlay"].polygon) == 5

    assert "geojson" in result
    assert result["geojson"].type == "FeatureCollection"
    assert len(result["geojson"].features) == 1
    feature = result["geojson"].features[0]
    assert feature.type == "Feature"
    assert feature.geometry.type == "Point"
    assert feature.geometry.coordinates == [78.4867, 17.385]
    assert feature.properties["risk_level"] == "HIGH"
    assert feature.properties["hazard"] == "flood"

    assert "timeline" in result
    assert len(result["timeline"]) == 1
    assert result["timeline"][0].event_type == "ANALYSIS_RUN"


def test_invalid_coordinates():
    with pytest.raises(ValueError, match="Latitude must be between -90 and 90"):
        visualization_service.generate_visualizations(
            lat=95.0, lon=78.4867, risk_level="HIGH", hazard_type="flood"
        )

    with pytest.raises(ValueError, match="Longitude must be between -180 and 180"):
        visualization_service.generate_visualizations(
            lat=17.385, lon=200.0, risk_level="HIGH", hazard_type="flood"
        )
