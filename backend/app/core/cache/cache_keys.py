import math


class CacheCategory:
    LOCATION_SEARCH = "location_search"
    SATELLITE_METADATA = "satellite_metadata"
    ANALYSIS_RESULTS = "analysis_results"
    RISK_ASSESSMENTS = "risk_assessments"
    ALERTS = "alerts"
    VISUALIZATION_OUTPUTS = "visualization_outputs"


class CacheKeyBuilder:
    VERSION = "v1"
    DEFAULT_ZOOM = 12

    @classmethod
    def build(cls, category: str, identifier: str) -> str:
        return f"{cls.VERSION}:{category}:{identifier}"

    @classmethod
    def location_search(cls, city: str) -> str:
        return cls.build(CacheCategory.LOCATION_SEARCH, city.lower().strip())

    @classmethod
    def spatial_tile(cls, category: str, z: int, x: int, y: int) -> str:
        return cls.build(category, f"tile:z{z}:x{x}:y{y}")

    @classmethod
    def coordinates(cls, category: str, lat: float, lon: float) -> str:
        z = cls.DEFAULT_ZOOM
        lat_rad = math.radians(lat)
        n = 2.0 ** z
        x = int((lon + 180.0) / 360.0 * n)
        y = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
        return cls.spatial_tile(category, z, x, y)
