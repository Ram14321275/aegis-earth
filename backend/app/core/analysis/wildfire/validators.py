from app.core.processing.models import AnalysisReadyDataset

class WildfireAnalysisValidator:
    @staticmethod
    def validate_ard(ard: AnalysisReadyDataset) -> None:
        """
        Validates that the ARD contains the necessary components for wildfire detection.
        """
        if ard.metadata.cloud_cover > 80.0:
            raise ValueError(f"Cloud cover too high for optical detection: {ard.metadata.cloud_cover}%")
            
        required_indices = {"NDVI", "NBR"}
        generated_indices = set(ard.metadata.indices_generated)
        
        missing = required_indices - generated_indices
        if missing:
            raise ValueError(f"Optical ARD is missing required indices for wildfire detection: {missing}")
