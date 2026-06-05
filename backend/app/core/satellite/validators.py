from datetime import datetime
from app.core.exceptions import ValidationError

def validate_timeseries_request(start_time: datetime, end_time: datetime) -> None:
    """Validates timeseries temporal bounds"""
    if start_time >= end_time:
        raise ValidationError("start_time must be before end_time")
    
    delta = end_time - start_time
    if delta.days > 365:
        raise ValidationError("timeseries request cannot exceed 365 days")
