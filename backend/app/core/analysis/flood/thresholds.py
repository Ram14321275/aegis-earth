import ee

# NDWI Thresholds
# Standard NDWI threshold for water is often > 0 or > 0.3 depending on region.
NDWI_WATER_THRESHOLD = 0.3

# SAR Thresholds (Sentinel-1 VV backscatter in dB)
# Typically backscatter < -15 dB is water
SAR_WATER_THRESHOLD_DB = -15.0

class ThresholdEvaluator:
    @staticmethod
    def get_ndwi_water_mask(ndwi_image: ee.Image) -> ee.Image:
        """
        Returns a binary mask where 1 represents water.
        """
        return ndwi_image.gt(NDWI_WATER_THRESHOLD)

    @staticmethod
    def get_sar_water_mask(sar_image: ee.Image, band: str = "VV") -> ee.Image:
        """
        Returns a binary mask where 1 represents water based on backscatter reduction.
        """
        return sar_image.select(band).lt(SAR_WATER_THRESHOLD_DB)
