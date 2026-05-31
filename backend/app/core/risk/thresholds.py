from typing import Any, Dict


class ThresholdConfig:
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def get_threshold(self, key: str, default: float) -> float:
        return self.config.get(key, default)


DEFAULT_THRESHOLDS = {
    "flood": {
        "water_coverage_high": 0.5,
        "growth_rate_high": 0.2,
    },
    "wildfire": {
        "burn_area_high": 100.0,
        "spread_rate_high": 10.0,
    },
}
