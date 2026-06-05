import ee

def apply_shadow_removal(image: ee.Image) -> ee.Image:
    """
    Removes cloud shadows.
    In a full production implementation, this calculates cloud projection geometry.
    For this ARD preprocessing layer, we apply a dark-pixel thresholding on the NIR/SWIR bands
    as a simplified shadow mask.
    """
    # Simplified shadow masking: if NIR (B8) is extremely low, it might be a shadow (or water)
    # We combine it with the QA60 cloud mask indirectly via upstream processing.
    nir = image.select('B8')
    shadow_mask = nir.gt(0.05) # Assume reflectance > 5% is non-shadow for land (rough MVP heuristic)
    
    return image.updateMask(shadow_mask).set("SHADOW_REMOVAL", "APPLIED")
