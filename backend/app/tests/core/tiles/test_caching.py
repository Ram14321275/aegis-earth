import pytest
from fastapi import Response
from app.core.tiles.caching.edge import edge_cache_manager

def test_edge_cache_headers_critical():
    response = Response()
    edge_cache_manager.set_tile_cache_headers(response, severity="CRITICAL", payload_bytes=b"test")
    
    assert response.headers["ETag"]
    assert response.headers["Vary"] == "X-Tenant-ID"
    assert "max-age=30" in response.headers["Cache-Control"]
    assert "stale-while-revalidate=120" in response.headers["Cache-Control"]

def test_edge_cache_headers_playback():
    response = Response()
    edge_cache_manager.set_tile_cache_headers(response, is_playback=True, payload_bytes=b"test")
    
    assert "immutable" in response.headers["Cache-Control"]
    assert "max-age=86400" in response.headers["Cache-Control"]
