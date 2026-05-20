export const STOP_META = {
  pretrip: { label: "Pre-trip", icon: "Wrench" },
  pickup: { label: "Pickup", icon: "Package" },
  dropoff: { label: "Dropoff", icon: "Flag" },
  fuel: { label: "Fuel", icon: "Fuel" },
  break: { label: "Break", icon: "Coffee" },
  rest: { label: "Rest", icon: "BedDouble" },
  duty_start: { label: "On duty", icon: "Play" },
};

export const MAP_WAYPOINTS = [
  { label: "A", color: "#16a34a" },
  { label: "P", color: "#d97706" },
  { label: "D", color: "#dc2626" },
];

export const MAP_STOP_TYPES = new Set(["break", "fuel", "rest"]);
