

from pathlib import Path
import base64
import html
import random
import unicodedata

from wdo.geometry.bbox import bbox_from_feature, _flatten_positions
from wdo.geometry.bearing import bearing_to_compass, initial_bearing
from wdo.geometry.distance import haversine_km, haversine_miles


ARROWS = {
    "N": "↑",
    "NE": "↗",
    "E": "→",
    "SE": "↘",
    "S": "↓",
    "SW": "↙",
    "W": "←",
    "NW": "↖",
}


DEFAULT_ALIASES = {
    "Antigua and Barbuda": "Antigua & Barbuda",
    "Bosnia and Herzegovina": "Bosnia & Herzegovina",
    "Brunei": "Brunei Darussalam",
    "Cape Verde": "Cabo Verde",
    "Cote d'Ivoire": "Côte d'Ivoire",
    "Czech Republic": "Czechia",
    "Democratic Republic of the Congo": "Congo, Democratic Republic of the",
    "Republic of Congo": "Congo",
    "Dominican Rep.": "Dominican Republic",
    "eSwatini": "Eswatini",
    "Faeroe Islands": "Faroe Islands",
    "Falkland Islands": "Falkland Islands (Malvinas)",
    "Iran": "Iran, Islamic Republic of",
    "Laos": "Lao People's Democratic Republic",
    "Macedonia": "North Macedonia",
    "Moldova": "Moldova, Republic of",
    "Palestine": "Palestine, State of",
    "Republic of Serbia": "Serbia",
    "Russia": "Russian Federation",
    "S. Sudan": "South Sudan",
    "Syria": "Syrian Arab Republic",
    "Taiwan": "Taiwan, Province of China",
    "Tanzania": "Tanzania, United Republic of",
    "The Bahamas": "Bahamas",
    "United States": "United States of America",
    "Vatican": "Holy See",
    "Venezuela": "Venezuela, Bolivarian Republic of",
    "Vietnam": "Viet Nam",
    "Aland": "Aland Islands",
    "French Southern and Antarctic Lands": "French Southern Territories",
    "Saint Barthelemy": "Saint Barthélemy",
    "Ivory Coast": "Côte d'Ivoire",
    "Republic of Congo": "Republic of the Congo",
    "Democratic Republic of the Congo": "Democratic Republic of the Congo",
    "Czech Republic": "Czech Republic",
    "Falkland Islands": "Falkland Islands",
    "Guinea Bissau": "Guinea-Bissau",
    "Hong Kong S.A.R.": "Hong Kong",
    "Iran": "Iran",
    "Laos": "Laos",
    "Macao S.A.R": "Macau",
    "Moldova": "Moldova",
    "Pitcairn Islands": "Pitcairn",
    "Palestine": "State of Palestine",
    "South Georgia and South Sandwich Islands": "South Georgia and the South Sandwich Islands",
    "Swaziland": "Eswatini",
    "Syria": "Syria",
    "East Timor": "Timor-Leste",
    "Taiwan": "Taiwan",
    "United Republic of Tanzania": "Tanzania",
    "Turkey": "Türkiye",
    "British Virgin Islands": "Virgin Islands (British)",
    "United States Virgin Islands": "Virgin Islands (U.S.)",
    "Venezuela": "Venezuela",
    "Vietnam": "Vietnam",
    "Russia": "Russia",
}


def _clean_name(name):
    """Normalize a country name for forgiving dictionary matching."""
    text = str(name).lower().replace("&", "and")
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    for char in ".,()'’":
        text = text.replace(char, " ")
    return " ".join(text.split())


def get_country_name(feature):
    """Return the country name from either supported polygon dataset."""
    props = feature.get("properties", {})
    return props.get("ADMIN") or props.get("name") or "Unknown"


def get_iso3(feature):
    """Return ISO-3 code from either supported polygon dataset."""
    props = feature.get("properties", {})
    return props.get("ISO_A3") or props.get("ISO3166-1-Alpha-3")


def get_iso2(feature):
    """Return ISO-2 code from either supported polygon dataset, lowercase when present."""
    props = feature.get("properties", {})
    iso2 = props.get("ISO_A2") or props.get("ISO3166-1-Alpha-2")
    return iso2.lower() if iso2 else None


def choose_target(features, seed=None):
    """Pick one feature at random. If seed is given, the pick is reproducible."""
    feature_list = list(features)
    if not feature_list:
        raise ValueError("Cannot choose a target from an empty feature list.")
    return random.Random(seed).choice(feature_list)


def feature_center(feature, method="bbox"):
    """Return a representative (lat, lon) for a Polygon/MultiPolygon feature.

    method="bbox" uses the center of the bounding box.
    method="mean" uses the mean of all boundary vertices.
    """
    if method == "bbox":
        min_lon, min_lat, max_lon, max_lat = bbox_from_feature(feature)
        return ((min_lat + max_lat) / 2, (min_lon + max_lon) / 2)

    if method == "mean":
        geometry = feature.get("geometry", {})
        coords = geometry.get("coordinates", [])
        positions = list(_flatten_positions(coords))
        if not positions:
            raise ValueError("Feature has no coordinates.")
        avg_lon = sum(pos[0] for pos in positions) / len(positions)
        avg_lat = sum(pos[1] for pos in positions) / len(positions)
        return (avg_lat, avg_lon)

    raise ValueError("method must be 'bbox' or 'mean'.")


def guess_feedback(guess_feature, target_feature):
    """Compare a guess to the target and return distance, bearing, compass, and arrow.

    The bearing points from the guessed country toward the target country.
    """
    guess_iso3 = get_iso3(guess_feature)
    target_iso3 = get_iso3(target_feature)
    guess_name = get_country_name(guess_feature)
    target_name = get_country_name(target_feature)

    correct = False
    if guess_iso3 and target_iso3 and guess_iso3 != "-99" and target_iso3 != "-99":
        correct = guess_iso3 == target_iso3
    else:
        correct = _clean_name(guess_name) == _clean_name(target_name)

    guess_center = feature_center(guess_feature)
    target_center = feature_center(target_feature)
    distance_km = haversine_km(guess_center, target_center)
    distance_mi = haversine_miles(guess_center, target_center)
    bearing_deg = initial_bearing(guess_center, target_center)
    compass = bearing_to_compass(bearing_deg)

    return {
        "correct": correct,
        "guess_name": guess_name,
        "target_name": target_name,
        "guess_iso3": guess_iso3,
        "target_iso3": target_iso3,
        "distance_km": distance_km,
        "distance_miles": distance_mi,
        "bearing_deg": bearing_deg,
        "compass": compass,
        "arrow": "🎯" if correct else ARROWS[compass],
    }


def format_feedback(result, units="km") -> str:
    """Return a plain-text version of guess feedback."""
    if result.get("correct"):
        return f"Correct! The target was {result.get('target_name')} 🎉"

    if units == "miles":
        distance = result["distance_miles"]
        unit_label = "mi"
    else:
        distance = result["distance_km"]
        unit_label = "km"

    return (
        f"{result.get('guess_name')}: "
        f"go {result['compass']} {result['arrow']} "
        f"about {distance:,.0f} {unit_label}"
    )


def build_country_lookup(countries_geojson, flag_index, flag_root="Resources/Data/flag-icons", aliases=None):
    """Return {iso3: {...}} by joining country polygons to flag metadata.

    The polygon data may already contain ISO-2 codes. When it does not, this function
    joins on country name and applies a small alias dictionary for common mismatches.
    Unmatched entries keep flag_path=None so the game can still run.
    """
    aliases = {**DEFAULT_ALIASES, **(aliases or {})}

    if isinstance(countries_geojson, dict):
        features = countries_geojson.get("features", [])
    else:
        features = list(countries_geojson)

    flag_by_iso2 = {item.get("code", "").lower(): item for item in flag_index}
    flag_by_name = {_clean_name(item.get("name")): item for item in flag_index}

    lookup = {}
    misses = []
    root = Path(flag_root)

    for feature in features:
        name = get_country_name(feature)
        iso3 = get_iso3(feature)
        if not iso3 or iso3 == "-99":
            continue

        iso2 = get_iso2(feature)
        flag_item = flag_by_iso2.get(iso2) if iso2 else None

        if flag_item is None:
            match_name = aliases.get(name, name)
            flag_item = flag_by_name.get(_clean_name(match_name))

        if flag_item:
            iso2 = flag_item.get("code")
            flag_path = str(root / flag_item.get("flag_4x3", ""))
        else:
            flag_path = None
            misses.append(name)

        lookup[iso3] = {
            "name": name,
            "iso2": iso2,
            "flag_path": flag_path,
        }

    return lookup, misses


def flag_img_html(flag_path, width=36):
    """Return an HTML img tag for an SVG flag path, using a portable data URI."""
    if not flag_path:
        return f"<span style='display:inline-block;width:{width}px;text-align:center'>🏳️</span>"

    path = Path(flag_path)
    if not path.exists():
        return f"<span style='display:inline-block;width:{width}px;text-align:center'>🏳️</span>"

    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return (
        f"<img src='data:image/svg+xml;base64,{encoded}' "
        f"width='{width}' style='border-radius:3px;border:1px solid #ddd'>"
    )


def proximity_label(distance_km):
    """Return a simple warm/cold label for one guess distance."""
    if distance_km < 500:
        return "🔥 close"
    if distance_km < 2000:
        return "🌡️ warm"
    return "🧊 cold"


def proximity_color(distance_km):
    """Return a color used by the guess-history UI."""
    if distance_km < 500:
        return "#2a9d8f"
    if distance_km < 2000:
        return "#f4a261"
    return "#457b9d"


def render_guess_row(country_name, flag_path, arrow, distance_km):
    """Return an HTML string for one row of the guess history."""
    safe_name = html.escape(country_name)
    color = proximity_color(distance_km)
    warmth = proximity_label(distance_km)
    flag = flag_img_html(flag_path)
    return f"""
    <div style="display:grid;grid-template-columns:48px 1fr 50px 120px 90px;
                align-items:center;gap:10px;padding:8px 10px;margin:6px 0;
                border:1px solid #e5e5e5;border-radius:10px;background:#ffffff;
                font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">
        <div>{flag}</div>
        <div style="font-weight:650;color:#1d3557">{safe_name}</div>
        <div style="font-size:24px;text-align:center;color:{color};font-weight:700">{arrow}</div>
        <div style="font-weight:650;text-align:right;color:{color}">{distance_km:,.0f} km</div>
        <div style="font-size:13px;color:#555;text-align:right">{warmth}</div>
    </div>
    """


class WorldleGame:
    """Small state object for a notebook-based Worldle game."""

    def __init__(self, features, seed=None, max_guesses=6):
        self.features = list(features)
        self.features_by_iso3 = {get_iso3(f): f for f in self.features if get_iso3(f)}
        self.target = choose_target(self.features, seed=seed)
        self.guesses = []
        self.max_guesses = max_guesses
        self.finished = False
        self.won = False

    def submit_guess(self, guess_iso3):
        """Submit a guess by ISO-3 code and return the feedback dict."""
        if self.finished:
            return {
                "correct": self.won,
                "message": "Game is already finished.",
                "target_name": get_country_name(self.target),
            }

        if guess_iso3 not in self.features_by_iso3:
            raise ValueError(f"Unknown ISO-3 code: {guess_iso3}")

        guess_feature = self.features_by_iso3[guess_iso3]
        feedback = guess_feedback(guess_feature, self.target)
        self.guesses.append(feedback)

        if feedback["correct"]:
            self.finished = True
            self.won = True
        elif len(self.guesses) >= self.max_guesses:
            self.finished = True

        return feedback

    def give_up(self):
        """End the game and reveal the target."""
        self.finished = True
        self.won = False
        return get_country_name(self.target)

    def result_string(self):
        """Return a compact shareable result string."""
        status = "won" if self.won else "lost"
        lines = [f"Worldle notebook: {status} in {len(self.guesses)}/{self.max_guesses}"]
        for fb in self.guesses:
            if fb["correct"]:
                lines.append("🎯 correct")
            else:
                lines.append(f"{fb['arrow']} {fb['distance_km']:,.0f} km")
        return "\n".join(lines)
