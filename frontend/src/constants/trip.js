export const DEFAULT_TRIP = {
  current_location: "Chicago, IL",
  pickup_location: "Indianapolis, IN",
  dropoff_location: "Nashville, TN",
  current_cycle_used: 12,
};

export const TRIP_FORM_FIELDS = [
  {
    name: "current_location",
    label: "Current location",
    placeholder: "Chicago, IL",
    type: "text",
    icon: "MapPin",
  },
  {
    name: "pickup_location",
    label: "Pickup",
    placeholder: "Indianapolis, IN",
    type: "text",
    icon: "Package",
  },
  {
    name: "dropoff_location",
    label: "Dropoff",
    placeholder: "Nashville, TN",
    type: "text",
    icon: "Flag",
  },
  {
    name: "current_cycle_used",
    label: "Cycle used (hours)",
    placeholder: "0",
    type: "number",
    icon: "Clock",
    min: 0,
    max: 70,
    step: 0.5,
    hint: "On-duty hours used in the current 8-day cycle",
  },
];
