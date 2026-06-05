from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class ProcessedRaster(BaseModel):
    id: str
    band_name: str
    geometry_wkt: str
    url: Optional[str] = None # Will point to cached/storage reference
    metadata: Dict[str, Any] = Field(default_factory=dict)

class DerivedIndex(BaseModel):
    name: str
    formula: str
    raster: ProcessedRaster

class ProcessingMetadata(BaseModel):
    source_collection: str
    acquisition_date: datetime
    cloud_cover: float
    processor_version: str
    indices_generated: List[str]
    processing_duration_ms: float
    provider_id: str
    scene_id: str
    filters_applied: List[str] = Field(default_factory=list)
    terrain_corrected: bool = False
    calibrated: bool = False

class AnalysisReadyDataset(BaseModel):
    ard_id: str
    scene_id: str
    rasters: List[ProcessedRaster]
    indices: List[DerivedIndex]
    metadata: ProcessingMetadata
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ProcessingResult(BaseModel):
    success: bool
    ard: Optional[AnalysisReadyDataset] = None
    error_message: Optional[str] = None
    execution_time_ms: float = 0.0
