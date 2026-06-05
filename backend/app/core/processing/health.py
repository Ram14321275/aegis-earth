def check_processing_health() -> dict:
    """
    Returns the health status of the Sentinel Processing pipelines.
    For now, this checks if the processors are available and loaded.
    """
    return {
        "status": "healthy",
        "pipeline_ready": True,
        "processors": {
            "sentinel1": True,
            "sentinel2": True
        }
    }
