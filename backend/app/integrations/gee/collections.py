from enum import Enum

class GEECollection(str, Enum):
    SENTINEL_1_SAR = "COPERNICUS/S1_GRD"
    SENTINEL_2_OPTICAL = "COPERNICUS/S2_SR_HARMONIZED"

# Default bands for our models
COLLECTION_BANDS = {
    GEECollection.SENTINEL_1_SAR: ["VV", "VH"],
    GEECollection.SENTINEL_2_OPTICAL: ["B2", "B3", "B4", "B8"] # Blue, Green, Red, NIR
}
