from typing import Any, Dict

from app.core.visualization.models import (
    GeoJSONFeature,
    GeoJSONFeatureCollection,
    GeoJSONGeometry,
)


def generate_point_feature(
    lat: float, lon: float, properties: Dict[str, Any]
) -> GeoJSONFeature:
    geometry = GeoJSONGeometry(type="Point", coordinates=[lon, lat])
    return GeoJSONFeature(geometry=geometry, properties=properties)


def generate_feature_collection(
    features: list[GeoJSONFeature],
) -> GeoJSONFeatureCollection:
    return GeoJSONFeatureCollection(features=features)
