from typing import Optional
from pydantic import BaseModel, Field, model_validator


class SearchRequest(BaseModel):
    query: Optional[str] = Field(None, description="City or location name")
    latitude: Optional[float] = Field(None, ge=-90.0, le=90.0, description="Latitude")
    longitude: Optional[float] = Field(None, ge=-180.0, le=180.0, description="Longitude")

    @model_validator(mode="after")
    def validate_search_inputs(self) -> "SearchRequest":
        has_query = bool(self.query and self.query.strip())
        has_lat = self.latitude is not None
        has_lon = self.longitude is not None
        has_coords = has_lat and has_lon

        if has_query and (has_lat or has_lon):
            raise ValueError(
                "Provide either 'query' or ('latitude' and 'longitude'), but not both."
            )
        if not has_query and not has_coords:
            raise ValueError("Provide either 'query' or ('latitude' and 'longitude').")
        if (has_lat and not has_lon) or (has_lon and not has_lat):
            raise ValueError("Both 'latitude' and 'longitude' must be provided together.")

        return self
