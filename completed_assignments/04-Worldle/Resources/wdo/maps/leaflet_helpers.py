"""Small ipyleaflet helper functions used by the Worldle notebook."""


def make_map(center=(0, 0), zoom=2, basemap=None, scroll_wheel_zoom=True):
    """Return an ipyleaflet.Map with sensible Worldle defaults."""
    from ipyleaflet import Map, basemaps

    if basemap is None:
        basemap = basemaps.OpenStreetMap.Mapnik

    return Map(
        center=center,
        zoom=zoom,
        basemap=basemap,
        scroll_wheel_zoom=scroll_wheel_zoom,
        layout={"height": "520px", "width": "100%"},
    )


def add_basemap(map_obj, name="OpenStreetMap"):
    """Add/select a basemap layer. Kept as a simple stub for later lessons."""
    return map_obj


def add_geojson(map_obj, data, name=None, style=None):
    """Add GeoJSON data to an ipyleaflet map and return the layer."""
    from ipyleaflet import GeoJSON

    if style is None:
        style = {
            "color": "#1d3557",
            "fillColor": "#e63946",
            "weight": 2,
            "fillOpacity": 0.55,
        }

    layer = GeoJSON(data=data, name=name or "GeoJSON", style=style)
    map_obj.add_layer(layer)
    return layer


def _features_from_geojson(data):
    """Return a list of features from Feature, FeatureCollection, or feature list."""
    if isinstance(data, dict) and data.get("type") == "FeatureCollection":
        return data.get("features", [])
    if isinstance(data, dict) and data.get("type") == "Feature":
        return [data]
    if isinstance(data, list):
        return data
    raise TypeError("Expected a GeoJSON Feature, FeatureCollection, or list of Features.")


def fit_map_to_geojson(map_obj, data):
    """Adjust map viewport to fit a GeoJSON feature or collection."""
    from wdo.geometry.bbox import bbox_from_features

    features = _features_from_geojson(data)
    min_lon, min_lat, max_lon, max_lat = bbox_from_features(features)
    map_obj.fit_bounds([[min_lat, min_lon], [max_lat, max_lon]])
    return map_obj


def add_layer_control(map_obj):
    """Add a layer control widget to the map."""
    from ipyleaflet import LayersControl

    control = LayersControl(position="topright")
    map_obj.add_control(control)
    return control


def add_scale_control(map_obj):
    """Add a scale control widget to the map."""
    from ipyleaflet import ScaleControl

    control = ScaleControl(position="bottomleft")
    map_obj.add_control(control)
    return control


def add_bbox(map_obj, bbox, **style):
    """Draw a bounding box on the map."""
    from ipyleaflet import Polygon

    min_lon, min_lat, max_lon, max_lat = bbox
    locations = [
        (min_lat, min_lon),
        (min_lat, max_lon),
        (max_lat, max_lon),
        (max_lat, min_lon),
    ]
    layer = Polygon(locations=locations, **style)
    map_obj.add_layer(layer)
    return layer


def add_path(map_obj, coords, **style):
    """Add a path/polyline to the map."""
    from ipyleaflet import Polyline

    layer = Polyline(locations=coords, **style)
    map_obj.add_layer(layer)
    return layer
