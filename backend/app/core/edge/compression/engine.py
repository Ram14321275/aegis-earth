import json
import gzip
from typing import Dict, Any, List

class EdgeCompressionEngine:
    """Bandwidth optimization that never mutates hazard lineage."""
    
    @staticmethod
    def compress_payload(data: List[Dict[str, Any]]) -> bytes:
        """Deterministically compresses a batch of events."""
        # Using separators to ensure deterministic JSON representation before compression
        serialized = json.dumps(data, sort_keys=True, separators=(',', ':'))
        return gzip.compress(serialized.encode('utf-8'))

    @staticmethod
    def decompress_payload(compressed_data: bytes) -> List[Dict[str, Any]]:
        """Decompresses back to original deterministic JSON."""
        decompressed = gzip.decompress(compressed_data)
        return json.loads(decompressed.decode('utf-8'))

compression_engine = EdgeCompressionEngine()
