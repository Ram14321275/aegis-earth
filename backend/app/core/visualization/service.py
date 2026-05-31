import time

from app.core.visualization.geojson import (
    generate_feature_collection,
    generate_point_feature,
)
from app.core.visualization.heatmaps import generate_heatmap
from app.core.visualization.overlays import generate_risk_overlay
from app.core.visualization.timelines import generate_timeline
from app.core.visualization.validators import validate_coordinates
from app.observability.metrics import metrics_store


class VisualizationService:
    def generate_visualizations(
        self, lat: float, lon: float, risk_level: str, hazard_type: str
    ):
        start_time = time.time()
        try:
            validate_coordinates(lat, lon)

            heatmap = generate_heatmap(lat, lon, intensity=0.8)
            overlay = generate_risk_overlay(lat, lon, risk_level)

            props = {"risk_level": risk_level, "hazard": hazard_type}
            feature = generate_point_feature(lat, lon, props)
            geojson = generate_feature_collection([feature])

            timeline_events = [
                {
                    "type": "ANALYSIS_RUN",
                    "description": "Analysis completed",
                    "metadata": {"hazard": hazard_type},
                }
            ]
            timeline = generate_timeline(timeline_events)

            metrics_store.record_visualization_request()
            duration_ms = (time.time() - start_time) * 1000
            metrics_store.record_visualization_duration(duration_ms)

            return {
                "heatmap": heatmap,
                "overlay": overlay,
                "geojson": geojson,
                "timeline": timeline,
            }
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            metrics_store.record_visualization_duration(duration_ms)
            raise e

    def get_status(self) -> dict:
        return {"status": "healthy"}


visualization_service = VisualizationService()
