from app.core.visualization.models import OverlayLayer


def generate_risk_overlay(lat: float, lon: float, risk_level: str) -> OverlayLayer:
    color = "#FF0000" if risk_level in ["HIGH", "CRITICAL"] else "#00FF00"
    polygon = [
        [lon - 0.01, lat - 0.01],
        [lon + 0.01, lat - 0.01],
        [lon + 0.01, lat + 0.01],
        [lon - 0.01, lat + 0.01],
        [lon - 0.01, lat - 0.01],
    ]
    return OverlayLayer(layer_id="risk-overlay", color=color, polygon=polygon)
