import math


def euclidean(p1, p2) -> float:
    """Naive planar distance between (lat, lon) points."""
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def haversine_km(p1, p2) -> float:
    """Great-circle distance in kilometers between (lat, lon) points."""
    lat1, lon1 = map(math.radians, p1)
    lat2, lon2 = map(math.radians, p2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return 6371.0 * c


def haversine_miles(p1, p2) -> float:
    """Great-circle distance in miles."""
    return haversine_km(p1, p2) * 0.621371


def compare_distance_methods(p1, p2):
    """Return both Euclidean and haversine results for comparison."""
    return {
        "euclidean_deg": euclidean(p1, p2),
        "haversine_km": haversine_km(p1, p2),
        "haversine_miles": haversine_miles(p1, p2),
    }


def distances_from_point(point, points):
    """Return distances from one point to many points."""
    return [haversine_km(point, p) for p in points]


def pairwise_distances(points):
    """Return pairwise distance matrix as nested lists."""
    return [[haversine_km(a, b) for b in points] for a in points]


def distance_to_feature(point, feature):
    """Distance from point to a representative point of a feature.

    Args:
        point: (lat, lon)
        feature: GeoJSON feature

    Returns:
        Great-circle distance in kilometers.
    """
    from wdo.geometry.bbox import bbox_from_feature

    min_lon, min_lat, max_lon, max_lat = bbox_from_feature(feature)

    feature_center = (
        (min_lat + max_lat) / 2,
        (min_lon + max_lon) / 2,
    )

    return haversine_km(point, feature_center)


def nearest_feature(point, features):
    """Return nearest feature and distance.

    Args:
        point: (lat, lon)
        features: list of GeoJSON features

    Returns:
        tuple: (nearest_feature, nearest_distance_km)
    """
    if not features:
        raise ValueError("features list is empty.")

    nearest = None
    nearest_distance = None

    for feature in features:
        distance = distance_to_feature(point, feature)

        if nearest_distance is None or distance < nearest_distance:
            nearest = feature
            nearest_distance = distance

    return nearest, nearest_distance