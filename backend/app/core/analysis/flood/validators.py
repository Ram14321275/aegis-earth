from app.core.processing.models import AnalysisReadyDataset

class FloodAnalysisValidator:
    @staticmethod
    def validate_ard(ard: AnalysisReadyDataset) -> None:
        """
        Validates that the ARD contains the necessary components for flood detection.
        """
        if ard.metadata.cloud_cover > 80.0:
            raise ValueError(f"Cloud cover too high for optical detection: {ard.metadata.cloud_cover}%")
            
        if "S2" in ard.metadata.source_collection:
            if "NDWI" not in ard.metadata.indices_generated:
                raise ValueError("Optical ARD is missing NDWI index required for flood detection.")
                
        if "S1" in ard.metadata.source_collection:
            if not ard.metadata.calibrated:
                raise ValueError("SAR ARD is not calibrated.")
