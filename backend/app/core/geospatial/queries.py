from sqlalchemy import func
from geoalchemy2.elements import WKTElement

def st_dwithin(column, wkt: str, radius_m: float):
    """
    Returns the SQLAlchemy condition for ST_DWithin.
    Expects SRID 4326 WKT string.
    """
    return func.ST_DWithin(column, func.ST_GeogFromText(wkt), radius_m)

def st_intersects(column, wkt: str):
    """
    Returns the SQLAlchemy condition for ST_Intersects.
    Expects SRID 4326 WKT string.
    """
    return func.ST_Intersects(column, func.ST_GeogFromText(wkt))

def st_contains(column, wkt: str):
    """
    Returns the SQLAlchemy condition for ST_Contains.
    Expects SRID 4326 WKT string.
    Note: ST_Contains is generally used with Geometry, but GeoAlchemy handles casts if needed.
    """
    # For Geography, ST_Covers or casting to Geometry might be needed in some cases,
    # but PostGIS supports ST_Intersects natively for Geography which is often preferred.
    # We will cast to Geometry for ST_Contains if strictly needed, or just use ST_Covers.
    return func.ST_Covers(func.ST_GeogFromText(wkt), column)

def st_distance(column1, wkt: str):
    """
    Returns the SQLAlchemy expression for ST_Distance.
    """
    return func.ST_Distance(column1, func.ST_GeogFromText(wkt))

def st_make_envelope(min_lon: float, min_lat: float, max_lon: float, max_lat: float, srid: int = 4326):
    """
    Returns the SQLAlchemy expression for ST_MakeEnvelope.
    """
    return func.ST_MakeEnvelope(min_lon, min_lat, max_lon, max_lat, srid)
