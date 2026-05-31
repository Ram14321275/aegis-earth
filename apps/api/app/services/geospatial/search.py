import re

from app.schemas.intelligence import Coordinates, ResolvedLocation

KNOWN_LOCATIONS: dict[str, Coordinates] = {
    "hyderabad": Coordinates(latitude=17.3850, longitude=78.4867),
    "mumbai": Coordinates(latitude=19.0760, longitude=72.8777),
    "delhi": Coordinates(latitude=28.6139, longitude=77.2090),
    "bengaluru": Coordinates(latitude=12.9716, longitude=77.5946),
    "bangalore": Coordinates(latitude=12.9716, longitude=77.5946),
    "chennai": Coordinates(latitude=13.0827, longitude=80.2707),
    "kolkata": Coordinates(latitude=22.5726, longitude=88.3639),
}

COORDINATE_PATTERN = re.compile(r"^\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*$")


def resolve_search(query: str) -> ResolvedLocation:
    cleaned = query.strip()
    coordinate_match = COORDINATE_PATTERN.match(cleaned)

    if coordinate_match:
        latitude = float(coordinate_match.group(1))
        longitude = float(coordinate_match.group(2))
        coordinates = Coordinates(latitude=latitude, longitude=longitude)
        return ResolvedLocation(
            location_name=f"{latitude:.4f}, {longitude:.4f}",
            coordinates=coordinates,
            source="coordinates",
        )

    key = cleaned.lower()
    coordinates = KNOWN_LOCATIONS.get(key, KNOWN_LOCATIONS["hyderabad"])
    location_name = cleaned.title() if key in KNOWN_LOCATIONS else f"{cleaned.title()} (nearest demo resolution)"

    return ResolvedLocation(location_name=location_name, coordinates=coordinates, source="city")

