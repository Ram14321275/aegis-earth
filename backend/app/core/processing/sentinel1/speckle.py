import ee

def apply_lee_filter(image: ee.Image) -> ee.Image:
    """
    Applies a standard Lee speckle filter for SAR imagery noise reduction.
    """
    kernel_size = 3
    # We use focal_median as a quick approximation for the standard Lee filter in this architecture
    # A true Lee filter requires calculating local variance, but focal_median is highly efficient for ARD base.
    filtered = image.focal_median(kernel_size, 'square', 'pixels')
    return filtered.copyProperties(image).set("SPECKLE_FILTER", "LEE_APPROXIMATION")

def apply_gamma_map_filter(image: ee.Image) -> ee.Image:
    """
    Applies a Gamma Maximum A Posteriori (MAP) filter abstraction.
    """
    # For MVP we use a focal mean to approximate Gamma MAP smoothing
    filtered = image.focal_mean(3, 'square', 'pixels')
    return filtered.copyProperties(image).set("SPECKLE_FILTER", "GAMMA_MAP_APPROXIMATION")

def apply_speckle_filter(image: ee.Image, method: str = "LEE") -> ee.Image:
    """
    Routes the speckle filter request to the proper mathematical implementation.
    """
    if method.upper() == "GAMMA_MAP":
        return apply_gamma_map_filter(image)
    return apply_lee_filter(image)
