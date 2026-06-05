import ee
import time
from typing import List
from datetime import datetime

from app.integrations.gee.client import GEEClient
from app.core.satellite.models import SatelliteScene
from app.core.processing.models import ProcessedRaster, DerivedIndex, ProcessingMetadata, AnalysisReadyDataset
from app.core.processing.sentinel2.cloudmask import apply_cloud_mask
from app.core.processing.sentinel2.shadows import apply_shadow_removal
from app.core.processing.sentinel2.indices import generate_all_indices

async def process_sentinel2_scene(scene: SatelliteScene) -> AnalysisReadyDataset:
    """
    Processes a raw Sentinel-2 scene into an Analysis-Ready Dataset (ARD).
    """
    start_time = time.time()
    
    def _execute_pipeline():
        image = ee.Image(scene.scene_id)
        
        # 1. Cloud Masking
        image = apply_cloud_mask(image)
        
        # 2. Shadow Removal
        image = apply_shadow_removal(image)
        
        # 3. Spectral Indices Generation
        indices = generate_all_indices(image)
        
        # We attach indices as bands to the main image to evaluate them collectively if needed
        # Or we evaluate their metadata explicitly.
        # Trigger computation to extract metadata and validate execution
        # A simple getInfo() on the base image ensures the graph is valid
        info = image.select(['B4', 'B8']).getInfo() 
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
            metadata={"cloud_masked": True, "shadows_removed": True}
        ))
        
    indices_list = [
        DerivedIndex(name="NDVI", formula="(NIR - RED) / (NIR + RED)", raster=ProcessedRaster(
            id=f"{scene.scene_id}_NDVI", band_name="NDVI", geometry_wkt=scene.geometry
        )),
        DerivedIndex(name="NDWI", formula="(GREEN - NIR) / (GREEN + NIR)", raster=ProcessedRaster(
            id=f"{scene.scene_id}_NDWI", band_name="NDWI", geometry_wkt=scene.geometry
        )),
        DerivedIndex(name="NBR", formula="(NIR - SWIR) / (NIR + SWIR)", raster=ProcessedRaster(
            id=f"{scene.scene_id}_NBR", band_name="NBR", geometry_wkt=scene.geometry
        ))
    ]
        
    metadata = ProcessingMetadata(
        source_collection="COPERNICUS/S2_SR_HARMONIZED",
        acquisition_date=scene.captured_at,
        cloud_cover=scene.cloud_cover,
        processor_version="1.0.0",
        indices_generated=["NDVI", "NDWI", "NBR"],
        processing_duration_ms=execution_ms,
        provider_id=scene.provider,
        scene_id=scene.scene_id,
        filters_applied=["CLOUD_MASK", "SHADOW_REMOVAL"],
        terrain_corrected=False,
        calibrated=True
    )
    
    ard = AnalysisReadyDataset(
        ard_id=f"ard_{scene.scene_id}",
        scene_id=scene.scene_id,
        rasters=rasters,
        indices=indices_list,
        metadata=metadata
    )
    
    return ard
