import ee
from typing import Dict, Any

def generate_ndvi(image: ee.Image) -> ee.Image:
    """
    Normalized Difference Vegetation Index (NDVI)
    Formula: (NIR - RED) / (NIR + RED)
    Sentinel-2 Bands: NIR = B8, RED = B4
    """
    ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
    return ndvi

def generate_ndwi(image: ee.Image) -> ee.Image:
    """
    Normalized Difference Water Index (NDWI)
    Formula: (GREEN - NIR) / (GREEN + NIR)
    Sentinel-2 Bands: GREEN = B3, NIR = B8
    """
    ndwi = image.normalizedDifference(['B3', 'B8']).rename('NDWI')
    return ndwi

def generate_nbr(image: ee.Image) -> ee.Image:
    """
    Normalized Burn Ratio (NBR)
    Formula: (NIR - SWIR) / (NIR + SWIR)
    Sentinel-2 Bands: NIR = B8, SWIR = B12 (or B11)
    We use B12 for standard NBR.
    """
    # Note: B12 might not be selected by default in some generic queries, 
    # but earthengine-api handles it if it's in the source collection.
    nbr = image.normalizedDifference(['B8', 'B12']).rename('NBR')
    return nbr

def generate_all_indices(image: ee.Image) -> Dict[str, ee.Image]:
    """
    Executes all spectral index generations.
    """
    return {
        "NDVI": generate_ndvi(image),
        "NDWI": generate_ndwi(image),
        "NBR": generate_nbr(image)
    }
