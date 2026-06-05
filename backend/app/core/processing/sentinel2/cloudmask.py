import ee

def apply_cloud_mask(image: ee.Image) -> ee.Image:
    """
    Masks clouds from Sentinel-2 SR imagery using the QA60 band.
    QA60 bit 10: Opaque clouds
    QA60 bit 11: Cirrus clouds
    """
    qa = image.select('QA60')
    
    # Bits 10 and 11 are clouds and cirrus, respectively.
    cloud_bit_mask = 1 << 10
    cirrus_bit_mask = 1 << 11
    
    # Both flags should be set to zero, indicating clear conditions.
    mask = qa.bitwiseAnd(cloud_bit_mask).eq(0).And(
        qa.bitwiseAnd(cirrus_bit_mask).eq(0)
    )
    
    # Return the masked image, scaled to surface reflectance
    return image.updateMask(mask).divide(10000).set("CLOUD_MASKING", "APPLIED")
