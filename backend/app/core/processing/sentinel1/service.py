import ee
import time
from typing import List
from datetime import datetime

from app.integrations.gee.client import GEEClient
from app.core.satellite.models import SatelliteScene
from app.core.processing.models import ProcessedRaster, ProcessingMetadata, AnalysisReadyDataset
from app.core.processing.sentinel1.calibration import calibrate_radiometry
from app.core.processing.sentinel1.speckle import apply_speckle_filter
from app.core.processing.sentinel1.terrain import apply_terrain_correction

async def process_sentinel1_scene(scene: SatelliteScene) -> AnalysisReadyDataset:
    """
    Processes a raw Sentinel-1 scene into an Analysis-Ready Dataset (ARD).
    """
    start_time = time.time()
    
    def _execute_pipeline():
        image = ee.Image(scene.scene_id)
        
        # 1. Radiometric Calibration
        image = calibrate_radiometry(image)
        
        # 2. Speckle Reduction
        image = apply_speckle_filter(image, method="LEE")
        
        # 3. Terrain Correction
        image = apply_terrain_correction(image)
        
        # Trigger computation to extract metadata and validate execution
        info = image.getInfo()
        return info
        
    info = await GEEClient.execute(_execute_pipeline)
    
    execution_ms = (time.time() - start_time) * 1000
    
    # Construct ARD structural models
    rasters = []
    for band in scene.bands:
        rasters.append(ProcessedRaster(
            id=f"{scene.scene_id}_{band}",
            band_name=band,
            geometry_wkt=scene.geometry,
            metadata={"filter": "LEE", "calibrated": True, "terrain_corrected": True}
        ))
        
    metadata = ProcessingMetadata(
        source_collection="COPERNICUS/S1_GRD",
        acquisition_date=scene.captured_at,
        cloud_cover=scene.cloud_cover,
        processor_version="1.0.0",
        indices_generated=[],
        processing_duration_ms=execution_ms,
        provider_id=scene.provider,
        scene_id=scene.scene_id,
        filters_applied=["LEE"],
        terrain_corrected=True,
        calibrated=True
    )
    
    ard = AnalysisReadyDataset(
        ard_id=f"ard_{scene.scene_id}",
        scene_id=scene.scene_id,
        rasters=rasters,
        indices=[],
        metadata=metadata
    )
    
    return ard
