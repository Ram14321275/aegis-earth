from app.core.geospatial.models import BoundingBox

MAX_AOI_SQ_KM = 5000.0 # Maximum allowed AOI to prevent OOM
MAX_TIMEOUT_MS = 60000.0 # 60 seconds max processing per scene

class ProcessingValidator:
    """
    Performance safeguards for Sentinel Processing Pipeline.
    """
    
    @staticmethod
    def validate_aoi_size(bbox: BoundingBox) -> bool:
        """
        Validates that the given bounding box does not exceed memory constraints.
        For MVP, we use a simple naive degree squared area check (approximate).
        1 degree ~ 111 km at equator.
        """
        width = bbox.max_lon - bbox.min_lon
        height = bbox.max_lat - bbox.min_lat
        
        # Approximate area in sq km
        approx_sq_km = (width * 111) * (height * 111)
        
        if approx_sq_km > MAX_AOI_SQ_KM:
            raise ValueError(f"AOI exceeds maximum processing size. Requested: {approx_sq_km:.2f} sq km, Max: {MAX_AOI_SQ_KM} sq km")
        return True

    @staticmethod
    def get_chunking_strategy(bbox: BoundingBox) -> int:
        """
        Abstraction: Returns the number of grid chunks an AOI should be split into.
        If Area > 1000 sq km, split into chunks.
        """
        width = bbox.max_lon - bbox.min_lon
        height = bbox.max_lat - bbox.min_lat
        approx_sq_km = (width * 111) * (height * 111)
        
        if approx_sq_km > 1000:
            return 4 # Split into 4 chunks
        return 1
