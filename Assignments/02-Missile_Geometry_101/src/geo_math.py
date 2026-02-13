"""
geo_math.py

Pure geometry + math helpers.
No file I/O.
No visualization.
No DataFrames.
"""

from __future__ import annotations
import math
from typing import Tuple, List


# ----------------------------------------
# Constants
# ----------------------------------------
EARTH_RADIUS_KM = 6371.0088  # mean Earth radius


# ----------------------------------------
# Distance: Haversine (km)
# ----------------------------------------
def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Compute great-circle distance between two lat/lon points.
    Returns distance in kilometers.
    """
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)

    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)

    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlmb / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return EARTH_RADIUS_KM * c


# ----------------------------------------
# Destination point (bearing + distance)
# ----------------------------------------
def destination_point(
    lat: float, lon: float, bearing_deg: float, distance_km: float
) -> Tuple[float, float]:
    """
    Compute destination lat/lon given:
      - start lat/lon
      - bearing in degrees
      - distance in km

    Uses great-circle formula.
    """
    bearing = math.radians(bearing_deg)

    lat1 = math.radians(lat)
    lon1 = math.radians(lon)
    d = distance_km / EARTH_RADIUS_KM

    lat2 = math.asin(
        math.sin(lat1) * math.cos(d) + math.cos(lat1) * math.sin(d) * math.cos(bearing)
    )

    lon2 = lon1 + math.atan2(
        math.sin(bearing) * math.sin(d) * math.cos(lat1),
        math.cos(d) - math.sin(lat1) * math.sin(lat2),
    )

    # normalize longitude to [-180, 180]
    lon2 = (math.degrees(lon2) + 540) % 360 - 180
    lat2 = math.degrees(lat2)

    return lat2, lon2


# ----------------------------------------
# Trajectory sampling (list of points)
# ----------------------------------------
def trajectory_points(
    origin_lat: float,
    origin_lon: float,
    bearing_deg: float,
    speed_kmh: float,
    duration_min: float,
    step_min: float = 2.0,
) -> List[Tuple[float, float]]:
    """
    Generate intermediate (lat, lon) points along a trajectory.
    """
    points = [(origin_lat, origin_lon)]

    steps = max(1, int(duration_min / step_min))
    for i in range(1, steps + 1):
        elapsed_hr = (i * step_min) / 60.0
        dist_km = speed_kmh * elapsed_hr
        lat2, lon2 = destination_point(origin_lat, origin_lon, bearing_deg, dist_km)
        points.append((lat2, lon2))

    return points
