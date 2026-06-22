import ee
from typing import Dict

def generate_ndvi(image: ee.Image) -> ee.Image:
    """
    Normalized Difference Vegetation Index (NDVI)
    Formula: (NIR - RED) / (NIR + RED)
    Sentinel-2 Bands: NIR = B8, RED = B4
    """
    return image.normalizedDifference(['B8', 'B4']).rename('NDVI')

def generate_ndwi(image: ee.Image) -> ee.Image:
    """
    Normalized Difference Water Index (NDWI)
    Formula: (GREEN - NIR) / (GREEN + NIR)
    Sentinel-2 Bands: GREEN = B3, NIR = B8
    """
    return image.normalizedDifference(['B3', 'B8']).rename('NDWI')

def generate_nbr(image: ee.Image) -> ee.Image:
    """
    Normalized Burn Ratio (NBR)
    Formula: (NIR - SWIR) / (NIR + SWIR)
    Sentinel-2 Bands: NIR = B8, SWIR = B12
    """
    return image.normalizedDifference(['B8', 'B12']).rename('NBR')

def generate_ndbi(image: ee.Image) -> ee.Image:
    """
    Normalized Difference Built-up Index (NDBI)
    Formula: (SWIR1 - NIR) / (SWIR1 + NIR)
    Sentinel-2 Bands: SWIR1 = B11, NIR = B8
    """
    return image.normalizedDifference(['B11', 'B8']).rename('NDBI')

def generate_all_indices(image: ee.Image) -> Dict[str, ee.Image]:
    """
    Executes all spectral index generations.
    """
    return {
        "NDVI": generate_ndvi(image),
        "NDWI": generate_ndwi(image),
        "NBR": generate_nbr(image),
        "NDBI": generate_ndbi(image)
    }
