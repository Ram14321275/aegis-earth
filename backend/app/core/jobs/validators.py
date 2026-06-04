from typing import Optional

from app.core.exceptions import ValidationError
from app.core.jobs.statuses import JobStatus

def validate_job_transition(current_status: str, next_status: JobStatus):
    valid_transitions = {
        JobStatus.PENDING: [JobStatus.QUEUED, JobStatus.CANCELLED, JobStatus.FAILED],
        JobStatus.QUEUED: [JobStatus.RUNNING, JobStatus.CANCELLED, JobStatus.FAILED],
        JobStatus.RUNNING: [JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.RETRYING, JobStatus.CANCELLED],
        JobStatus.RETRYING: [JobStatus.QUEUED, JobStatus.CANCELLED, JobStatus.FAILED],
        JobStatus.COMPLETED: [],
        JobStatus.FAILED: [],
        JobStatus.CANCELLED: []
    }
    
    if next_status not in valid_transitions.get(current_status, []):
        raise ValidationError(f"Invalid transition from {current_status} to {next_status}")

def validate_analysis_type(analysis_type: str):
    valid_types = ["flood", "wildfire", "earthquake", "cyclone"]
    if analysis_type not in valid_types:
        raise ValidationError(f"Unsupported analysis type: {analysis_type}")
