export const DUTY_ROWS = [
  { key: "off_duty", label: "Off Duty", color: "#64748b" },
  { key: "sleeper", label: "Sleeper Berth", color: "#7c3aed" },
  { key: "driving", label: "Driving", color: "#16a34a" },
  { key: "on_duty", label: "On Duty (Not Driving)", color: "#d97706" },
];

export const GRID = {
  left: 88,
  width: 720,
  rowHeight: 28,
  minutesPerDay: 1440,
};

export const HOUR_TICKS = [0, 4, 8, 12, 16, 20, 24];

export function minuteToX(minute) {
  return GRID.left + (minute / GRID.minutesPerDay) * GRID.width;
}

export function hourLabel(hour) {
  if (hour === 0 || hour === 24) return "Mid";
  if (hour === 12) return "Noon";
  return String(hour);
}
