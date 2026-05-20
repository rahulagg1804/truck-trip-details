from typing import Any

import requests

OSRM_URL = "https://router.project-osrm.org/route/v1/driving"


def get_route(waypoints: list[dict[str, Any]]) -> dict[str, Any]:
    if len(waypoints) < 2:
        raise ValueError("At least two waypoints required")

    coords = ";".join(f"{wp['lng']},{wp['lat']}" for wp in waypoints)
    url = f"{OSRM_URL}/{coords}"
    resp = requests.get(
        url,
        params={
            "overview": "full",
            "geometries": "geojson",
            "steps": "true",
            "annotations": "distance,duration",
        },
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != "Ok" or not data.get("routes"):
        raise ValueError(f"Routing failed: {data.get('message', 'unknown error')}")

    route = data["routes"][0]
    legs = []
    for i, leg in enumerate(route["legs"]):
        legs.append(
            {
                "from": waypoints[i]["short_label"] or waypoints[i]["label"],
                "to": waypoints[i + 1]["short_label"] or waypoints[i + 1]["label"],
                "distance_miles": leg["distance"] / 1609.34,
                "duration_hours": leg["duration"] / 3600,
            }
        )

    return {
        "geometry": route["geometry"],
        "distance_miles": route["distance"] / 1609.34,
        "duration_hours": route["duration"] / 3600,
        "legs": legs,
        "waypoints": [
            {"lat": wp["lat"], "lng": wp["lng"], "label": wp.get("short_label") or wp["label"]}
            for wp in waypoints
        ],
    }
