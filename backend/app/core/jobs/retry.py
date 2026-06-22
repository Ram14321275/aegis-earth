import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class RetryManager:
    def __init__(self, base_delay_seconds: int = 2, max_retries: int = 3):
        self.base_delay_seconds = base_delay_seconds
        self.max_retries = max_retries

    def calculate_backoff(self, current_retry_count: int) -> int:
        """
        Deterministic exponential backoff: delay = base * 2^retry_count
        """
        return self.base_delay_seconds * (2 ** current_retry_count)

    def should_retry(self, current_retry_count: int, job_max_retries: int = None) -> bool:
        max_allowed = job_max_retries if job_max_retries is not None else self.max_retries
        return current_retry_count < max_allowed

retry_manager = RetryManager()
