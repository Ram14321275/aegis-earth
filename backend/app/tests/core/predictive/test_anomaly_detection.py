import pytest
from app.core.predictive.anomaly_detection.detector import anomaly_detector

@pytest.mark.asyncio
async def test_anomaly_detection():
    anomalies = await anomaly_detector.detect_anomalies()
    assert len(anomalies) > 0
    assert anomalies[0].explainability is not None
