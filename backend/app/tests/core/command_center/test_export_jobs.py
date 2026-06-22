import pytest
from fastapi import HTTPException
from app.core.command_center.exports.service import command_center_export_service

@pytest.mark.asyncio
async def test_export_invalid_format():
    with pytest.raises(HTTPException) as excinfo:
        await command_center_export_service.request_export("tenant1", "snap-1", "docx")
    assert excinfo.value.status_code == 400

@pytest.mark.asyncio
async def test_export_invalid_snapshot():
    with pytest.raises(HTTPException) as excinfo:
        await command_center_export_service.request_export("tenant1", "nonexistent-snap", "json")
    assert excinfo.value.status_code == 404
