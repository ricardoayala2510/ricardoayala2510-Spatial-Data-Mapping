
"""geo.py — a minimal geodetic utility module."""
from math import radians, degrees, sin, cos, asin, atan2, sqrt

EARTH_RADIUS_KM = 6371.0088  # mean radius — write this constant ONCE


def haversine_km(lat1, lon1, lat2, lon2):
    """
    Great-circle distance between two points.
    Inputs: degrees.  Output: kilometers.
    """
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi   = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)
    a = sin(dphi/2)**2 + cos(phi1)*cos(phi2)*sin(dlambda/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return EARTH_RADIUS_KM * c
