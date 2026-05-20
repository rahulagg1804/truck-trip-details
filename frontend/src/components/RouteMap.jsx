import { useMemo } from "react";
import { MapContainer, TileLayer, Polyline, Marker, Popup } from "react-leaflet";
import L from "leaflet";
import { MAP_WAYPOINTS, MAP_STOP_TYPES } from "../constants/stops";

function createMarkerIcon(color, label) {
  return L.divIcon({
    className: "",
    html: `<div style="background:${color};color:#fff;width:22px;height:22px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:bold;border:1px solid #fff">${label}</div>`,
    iconSize: [22, 22],
    iconAnchor: [11, 11],
  });
}

export default function RouteMap({ route, stops = [] }) {
  const positions = useMemo(() => {
    if (!route?.geometry?.coordinates) return [];
    return route.geometry.coordinates.map(([lng, lat]) => [lat, lng]);
  }, [route]);

  const center = useMemo(() => {
    if (!positions.length) return [39, -98];
    return L.latLngBounds(positions).getCenter();
  }, [positions]);

  if (!positions.length) {
    return (
      <div className="h-72 flex items-center justify-center text-slate-500 text-sm">
        No route data
      </div>
    );
  }

  const restStops = stops.filter((s) => MAP_STOP_TYPES.has(s.type));

  return (
    <MapContainer
      center={[center.lat, center.lng]}
      zoom={6}
      className="h-72 w-full"
      scrollWheelZoom={false}
    >
      <TileLayer
        attribution='&copy; <a href="https://openstreetmap.org">OSM</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <Polyline positions={positions} pathOptions={{ color: "#d97706", weight: 3 }} />
      {route.waypoints?.map((wp, index) => {
        const marker = MAP_WAYPOINTS[index] || { label: "?", color: "#94a3b8" };
        return (
          <Marker
            key={`wp-${index}`}
            position={[wp.lat, wp.lng]}
            icon={createMarkerIcon(marker.color, marker.label)}
          >
            <Popup>{wp.label}</Popup>
          </Marker>
        );
      })}
      {restStops.map((stop, index) => (
        <Marker
          key={`stop-${stop.type}-${index}`}
          position={[stop.lat, stop.lng]}
          icon={createMarkerIcon("#6366f1", "·")}
        >
          <Popup>
            {stop.description}
            <br />
            {stop.location}
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}
