


def _geometry_coordinates(feature_or_geometry):
    """Return the coordinates list from a GeoJSON Feature or Geometry."""
    if not isinstance(feature_or_geometry, dict):
        raise TypeError("Expected a GeoJSON Feature or Geometry dictionary.")

    if feature_or_geometry.get("type") == "Feature":
        geometry = feature_or_geometry.get("geometry", {})
    else:
        geometry = feature_or_geometry

    return geometry.get("type"), geometry.get("coordinates", [])


def _flatten_positions(coords):
    """Yield every [lon, lat] position from nested GeoJSON coordinates."""
    if not coords:
        return

    first = coords[0]
    if isinstance(first, (int, float)):
        if len(coords) >= 2:
            yield (coords[0], coords[1])
    else:
        for item in coords:
            yield from _flatten_positions(item)


def bbox_from_points(points):
    """Return bbox as (min_lon, min_lat, max_lon, max_lat) from (lat, lon) points."""
    lats = [p[0] for p in points]
    lons = [p[1] for p in points]
    return (min(lons), min(lats), max(lons), max(lats))


def bbox_from_feature(feature):
    """Return (min_lon, min_lat, max_lon, max_lat) for a GeoJSON feature.

    Supports Polygon and MultiPolygon geometries. Coordinates in GeoJSON are stored
    as [longitude, latitude], so the returned bbox uses lon/lat order.
    """
    geom_type, coords = _geometry_coordinates(feature)
    if geom_type not in {"Polygon", "MultiPolygon"}:
        raise ValueError(f"Unsupported geometry type for bbox: {geom_type}")

    positions = list(_flatten_positions(coords))
    if not positions:
        raise ValueError("Feature has no coordinates.")

    lons = [pos[0] for pos in positions]
    lats = [pos[1] for pos in positions]
    return (min(lons), min(lats), max(lons), max(lats))


def bbox_from_features(features):
    """Compute one bbox across many GeoJSON features or a FeatureCollection."""
    if isinstance(features, dict) and features.get("type") == "FeatureCollection":
        feature_list = features.get("features", [])
    else:
        feature_list = list(features)

    if not feature_list:
        raise ValueError("No features supplied.")

    boxes = [bbox_from_feature(feature) for feature in feature_list]
    return (
        min(box[0] for box in boxes),
        min(box[1] for box in boxes),
        max(box[2] for box in boxes),
        max(box[3] for box in boxes),
    )


def bbox_to_polygon(bbox):
    """Convert bbox tuple into a closed polygon coordinate list as (lat, lon)."""
    min_lon, min_lat, max_lon, max_lat = bbox
    return [
        (min_lat, min_lon),
        (min_lat, max_lon),
        (max_lat, max_lon),
        (max_lat, min_lon),
        (min_lat, min_lon),
    ]
