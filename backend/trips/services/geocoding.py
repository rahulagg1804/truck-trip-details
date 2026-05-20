import time
from typing import Any

import requests
from django.conf import settings

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
_LAST_REQUEST = 0.0


def _throttle():
    global _LAST_REQUEST
    elapsed = time.time() - _LAST_REQUEST
    if elapsed < 1.1:
        time.sleep(1.1 - elapsed)
    _LAST_REQUEST = time.time()


def geocode(query: str) -> dict[str, Any]:
    query = query.strip()
    if not query:
        raise ValueError("Location cannot be empty")

    if "," in query:
        parts = [p.strip() for p in query.split(",", 1)]
        if len(parts) == 2:
            try:
                lat, lng = float(parts[0]), float(parts[1])
                label = _reverse_label(lat, lng) if settings.GEOCODING_ENABLED else f"{lat:.4f}, {lng:.4f}"
                return {
                    "lat": lat,
                    "lng": lng,
                    "label": label,
                    "short_label": label,
                    "query": query,
                }
            except ValueError:
                pass

    if not settings.GEOCODING_ENABLED:
        raise ValueError(
            f"Could not parse coordinates from '{query}'. "
            "Use 'latitude, longitude' or enable geocoding."
        )

    _throttle()
    resp = requests.get(
        NOMINATIM_URL,
        params={"q": query, "format": "json", "limit": 1, "countrycodes": "us"},
        headers={"User-Agent": "TruckTripPlanner/1.0"},
        timeout=15,
    )
    resp.raise_for_status()
    results = resp.json()
    if not results:
        raise ValueError(f"Could not find location: {query}")

    item = results[0]
    lat, lng = float(item["lat"]), float(item["lon"])
    label = item.get("display_name", query)
    short = _short_label(item)
    return {
        "lat": lat,
        "lng": lng,
        "label": label,
        "short_label": short,
        "query": query,
    }


def _reverse_label(lat: float, lng: float) -> str:
    _throttle()
    resp = requests.get(
        "https://nominatim.openstreetmap.org/reverse",
        params={"lat": lat, "lon": lng, "format": "json"},
        headers={"User-Agent": "TruckTripPlanner/1.0"},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    return _short_label(data.get("address", {})) or data.get("display_name", f"{lat:.4f}, {lng:.4f}")


def _short_label(item: dict) -> str:
    if isinstance(item, dict) and "address" in item:
        addr = item["address"]
    elif isinstance(item, dict) and ("city" in item or "town" in item):
        addr = item
    else:
        display = item.get("display_name", "") if isinstance(item, dict) else str(item)
        parts = [p.strip() for p in display.split(",")[:3]]
        return ", ".join(parts) if parts else display

    city = (
        addr.get("city")
        or addr.get("town")
        or addr.get("village")
        or addr.get("hamlet")
        or addr.get("county", "")
    )
    state = addr.get("state", "")
    if city and state:
        abbr = _state_abbr(state)
        return f"{city}, {abbr}"
    return city or state or "Unknown"


def _state_abbr(state: str) -> str:
    states = {
        "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
        "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
        "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
        "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
        "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
        "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
        "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
        "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
        "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
        "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
        "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
        "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
        "Wisconsin": "WI", "Wyoming": "WY", "District of Columbia": "DC",
    }
    if len(state) == 2:
        return state.upper()
    return states.get(state, state[:2].upper() if state else "")
