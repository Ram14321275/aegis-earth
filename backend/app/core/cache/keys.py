class CacheCategory:
    LOCATION_SEARCH = "location_search"
    SATELLITE_METADATA = "satellite_metadata"
    ANALYSIS_RESULTS = "analysis_results"
    RISK_ASSESSMENTS = "risk_assessments"
    ALERTS = "alerts"


class CacheKeyBuilder:
    VERSION = "v1"

    @classmethod
    def build(cls, category: str, identifier: str) -> str:
        return f"{cls.VERSION}:{category}:{identifier}"

    @classmethod
    def location_search(cls, city: str) -> str:
        return cls.build(CacheCategory.LOCATION_SEARCH, city.lower().strip())

    @classmethod
    def coordinates(cls, category: str, lat: float, lon: float) -> str:
        return cls.build(category, f"{lat:.4f}:{lon:.4f}")
