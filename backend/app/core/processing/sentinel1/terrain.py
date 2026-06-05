import ee

def apply_terrain_correction(image: ee.Image) -> ee.Image:
    """
    Applies Range-Doppler Terrain Correction to Sentinel-1 imagery.
    GEE provides Sentinel-1 ARD pre-orthorectified using SRTM/ASTER DEM.
    However, shadows and layover masks can be applied here to further refine the ARD.
    """
    # For MVP, we pass through the orthorectified image but tag it properly
    return image.set("TERRAIN_CORRECTION", "APPLIED")
