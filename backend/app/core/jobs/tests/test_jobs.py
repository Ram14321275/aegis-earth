import pytest
from app.core.jobs.retry import retry_manager
from app.core.jobs.scheduler import job_scheduler

def test_retry_manager_exponential_backoff():
    assert retry_manager.calculate_backoff(0) == 2
    assert retry_manager.calculate_backoff(1) == 4
    assert retry_manager.calculate_backoff(2) == 8
    
def test_retry_manager_should_retry():
    assert retry_manager.should_retry(0, job_max_retries=3) is True
    assert retry_manager.should_retry(3, job_max_retries=3) is False

def test_priority_scheduler_scoring_critical():
    payload = {
        "metadata_data": {
            "severity": "CRITICAL",
            "population_density": 15000,
            "tenant_tier": "enterprise",
            "is_urgent": True
        }
    }
    score = job_scheduler._calculate_priority(payload)
    # 40 (Critical) + 30 (>10k) + 20 (enterprise) + 10 (urgent) = 100
    assert score == 100.0

def test_priority_scheduler_scoring_low():
    payload = {
        "metadata_data": {
            "severity": "LOW",
            "population_density": 50,
            "tenant_tier": "standard",
            "is_urgent": False
        }
    }
    score = job_scheduler._calculate_priority(payload)
    # 0 + 0 + 0 + 0 = 0
    assert score == 0.0
