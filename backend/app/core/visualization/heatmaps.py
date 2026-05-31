from app.core.visualization.models import HeatmapDataPoint, HeatmapLayer


def generate_heatmap(lat: float, lon: float, intensity: float) -> HeatmapLayer:
    points = [HeatmapDataPoint(lat=lat, lon=lon, intensity=intensity)]
    return HeatmapLayer(layer_id="heatmap-01", points=points)
