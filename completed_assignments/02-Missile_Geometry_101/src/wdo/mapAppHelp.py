import json
from pathlib import Path

from ipyleaflet import Map, Marker, LayersControl, WidgetControl
import ipywidgets as widgets
from IPython.display import display


class GeoJsonHelp:
    """
    Helper class for loading and inspecting GeoJSON files.
    """

    def __init__(self, path: Path = None):
        self.geojson_obj = None
        self.path = path
        if self.path:
            self.load_geojson(self.path)

    def load_geojson(self, path: Path):
        """
        Load a GeoJSON file and return the parsed object.
        """
        if not path.exists():
            raise FileNotFoundError(
                f"\nFile not found:\n{path}\n"
                "Check spelling and folder structure."
            )

        self.geojson_obj = json.loads(path.read_text())
        return self.geojson_obj

    def get_features(self, geojson_obj=None):
        """
        Return the list of features from a GeoJSON FeatureCollection.
        """
        if geojson_obj is None:
            geojson_obj = self.geojson_obj
        return geojson_obj.get("features", [])

    def extract_polygon_rings(self, feature):
        """
        Return a flat list of rings from Polygon or MultiPolygon geometry.
        """
        geom = feature["geometry"]
        coords = geom["coordinates"]

        if geom["type"] == "Polygon":
            return coords

        if geom["type"] == "MultiPolygon":
            rings = []
            for poly in coords:
                rings.extend(poly)
            return rings

        return []


class MapAppHelp:
    def __init__(self, points_file: Path, center=(40.0, -99.0), zoom=5):
        self.points_file = points_file
        self.clicked_points = self.load_points()
        self.markers = []

        self.map = Map(
            center=center,
            zoom=zoom,
            layout=widgets.Layout(width="100%", height="700px"),
        )
        self.map.add(LayersControl())

        self.output = widgets.Output()
        self.clear_btn = widgets.Button(description="Clear Saved Points")

        self.restore_markers()
        self.bind_events()
        self.add_controls()

    def load_points(self):
        """
        Load saved points from disk, or create an empty file if needed.
        """
        if self.points_file.exists():
            text = self.points_file.read_text().strip()
            if text:
                return json.loads(text)
            return []

        self.points_file.parent.mkdir(parents=True, exist_ok=True)
        self.points_file.write_text("[]")
        return []

    def save_points(self):
        """
        Save the current clicked points list to disk.
        """
        self.points_file.parent.mkdir(parents=True, exist_ok=True)
        self.points_file.write_text(json.dumps(self.clicked_points, indent=2))

    def restore_markers(self):
        """
        Rebuild markers from previously saved points.
        """
        for pt in self.clicked_points:
            marker = Marker(location=(pt["lat"], pt["lon"]))
            self.markers.append(marker)
            self.map.add(marker)

    def add_marker(self, lat: float, lon: float):
        """
        Add a marker to the map and track it internally.
        """
        marker = Marker(location=(lat, lon))
        self.markers.append(marker)
        self.map.add(marker)

    def log(self, message: str):
        """
        Print a message to the notebook output widget.
        """
        with self.output:
            print(message)

    def handle_interaction(self, **kwargs):
        """
        Map click callback required by ipyleaflet.
        """
        if kwargs.get("type") != "click":
            return

        lat, lon = kwargs["coordinates"]
        point = {"lat": round(lat, 6), "lon": round(lon, 6)}

        self.clicked_points.append(point)
        self.add_marker(point["lat"], point["lon"])
        self.save_points()
        self.log(f"Saved click: {point}")

    def clear_points(self, _):
        """
        Button callback required by ipywidgets.
        """
        self.clicked_points.clear()
        self.save_points()

        for marker in self.markers:
            try:
                self.map.remove(marker)
            except Exception:
                pass

        self.markers.clear()
        self.log("Cleared saved points.")

    def bind_events(self):
        """
        Attach callbacks to the map and button.
        """
        self.map.on_interaction(self.handle_interaction)
        self.clear_btn.on_click(self.clear_points)

    def add_controls(self):
        """
        Add UI controls to the map.
        """
        self.map.add(WidgetControl(widget=self.clear_btn, position="topright"))

    def display(self):
        """
        Show the map and output area.
        """
        display(self.map, self.output)
