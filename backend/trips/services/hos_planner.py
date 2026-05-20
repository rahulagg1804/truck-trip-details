from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any

from django.conf import settings
from django.utils import timezone

OFF_DUTY = "off_duty"
SLEEPER = "sleeper"
DRIVING = "driving"
ON_DUTY = "on_duty"

MAX_DRIVING_HRS = 11.0
MAX_WINDOW_HRS = 14.0
BREAK_AFTER_DRIVING_HRS = 8.0
BREAK_DURATION_HRS = 0.5
RESET_HRS = 10.0
PRE_TRIP_HRS = 0.5


@dataclass
class Segment:
    status: str
    start: datetime
    end: datetime
    location: str
    remark: str = ""
    lat: float | None = None
    lng: float | None = None
    miles: float = 0.0


@dataclass
class PlannerState:
    current_time: datetime
    window_start: datetime | None = None
    driving_in_window: float = 0.0
    driving_since_break: float = 0.0
    cycle_used: float = 0.0
    miles_since_fuel: float = 0.0
    segments: list[Segment] = field(default_factory=list)
    stops: list[dict[str, Any]] = field(default_factory=list)
    miles_driven_today: float = 0.0
    day_miles: dict[str, float] = field(default_factory=dict)


def plan_trip(
    *,
    route: dict[str, Any],
    waypoints: list[dict[str, Any]],
    cycle_used_hours: float,
    start_time: datetime | None = None,
) -> dict[str, Any]:
    speed = settings.AVERAGE_SPEED_MPH
    fuel_interval = settings.FUEL_INTERVAL_MILES
    pickup_dropoff_hrs = settings.PICKUP_DROPOFF_HOURS

    leg_distances = [leg["distance_miles"] for leg in route["legs"]]
    total_miles = route["distance_miles"]
    leg_ends = []
    acc = 0.0
    for d in leg_distances:
        acc += d
        leg_ends.append(acc)

    if start_time is None:
        now = timezone.now()
        start_time = now.replace(hour=6, minute=0, second=0, microsecond=0)
        if start_time < now:
            start_time += timedelta(days=1)

    state = PlannerState(current_time=start_time, cycle_used=cycle_used_hours)

    progress = 0.0
    phase_idx = 0  # 0=to pickup, 1=at pickup, 2=to dropoff, 3=at dropoff
    phases = ["to_pickup", "at_pickup", "to_dropoff", "at_dropoff"]

    def location_at(p: float) -> tuple[str, float, float]:
        frac = p / total_miles if total_miles else 0
        frac = max(0.0, min(1.0, frac))
        coords = route["geometry"]["coordinates"]
        idx = int(frac * (len(coords) - 1))
        lng, lat = coords[idx]
        if frac < leg_ends[0] / total_miles if total_miles else True:
            label = waypoints[0].get("short_label") or waypoints[0]["label"]
        elif frac < (leg_ends[1] / total_miles if len(leg_ends) > 1 and total_miles else 1):
            label = waypoints[1].get("short_label") or waypoints[1]["label"]
        else:
            label = waypoints[-1].get("short_label") or waypoints[-1]["label"]
        return label, lat, lng

    def check_cycle():
        if state.cycle_used >= settings.CYCLE_LIMIT_HOURS:
            _take_reset(state, location_at(progress), "70-hour/8-day cycle limit — 34-hour restart")
            return True
        return False

    def start_window(loc: str, lat: float, lng: float):
        if state.window_start is None:
            state.window_start = state.current_time
            _add_stop(state, "duty_start", loc, lat, lng, "14-hour driving window begins")

    def window_elapsed() -> float:
        if state.window_start is None:
            return 0.0
        return (state.current_time - state.window_start).total_seconds() / 3600

    def take_break_if_needed(loc: str, lat: float, lng: float):
        if state.driving_since_break >= BREAK_AFTER_DRIVING_HRS - 0.01:
            _add_stop(state, "break", loc, lat, lng, "30-minute break")
            _add_segment(state, OFF_DUTY, state.current_time, state.current_time + timedelta(hours=BREAK_DURATION_HRS), loc, "30-minute break")
            state.current_time += timedelta(hours=BREAK_DURATION_HRS)
            state.driving_since_break = 0.0

    def take_reset_if_needed(loc: str, lat: float, lng: float):
        need_reset = (
            state.driving_in_window >= MAX_DRIVING_HRS - 0.01
            or window_elapsed() >= MAX_WINDOW_HRS - 0.01
        )
        if need_reset:
            reason = "11-hour driving limit" if state.driving_in_window >= MAX_DRIVING_HRS - 0.01 else "14-hour window limit"
            _take_reset(state, (loc, lat, lng), reason)
            return True
        return False

    def fuel_if_needed(loc: str, lat: float, lng: float):
        if state.miles_since_fuel >= fuel_interval:
            _add_stop(state, "fuel", loc, lat, lng, f"Fuel stop (every {fuel_interval} mi)")
            _add_segment(
                state,
                ON_DUTY,
                state.current_time,
                state.current_time + timedelta(hours=0.5),
                loc,
                "Fueling",
            )
            state.current_time += timedelta(hours=0.5)
            state.cycle_used += 0.5
            state.miles_since_fuel = 0.0

    # pre-trip
    loc0, lat0, lng0 = location_at(0)
    start_window(loc0, lat0, lng0)
    _add_stop(state, "pretrip", loc0, lat0, lng0, "Pre-trip inspection")
    _add_segment(state, ON_DUTY, state.current_time, state.current_time + timedelta(hours=PRE_TRIP_HRS), loc0, "Pre-trip inspection")
    state.current_time += timedelta(hours=PRE_TRIP_HRS)
    state.cycle_used += PRE_TRIP_HRS

    while phase_idx < len(phases):
        phase = phases[phase_idx]
        target_progress = leg_ends[0] if phase in ("to_pickup", "at_pickup") else leg_ends[-1]

        if phase == "at_pickup":
            loc, lat, lng = location_at(leg_ends[0])
            _add_stop(state, "pickup", loc, lat, lng, "Pickup — load freight (1 hr)")
            _add_segment(
                state,
                ON_DUTY,
                state.current_time,
                state.current_time + timedelta(hours=pickup_dropoff_hrs),
                loc,
                "Pickup and loading",
            )
            state.current_time += timedelta(hours=pickup_dropoff_hrs)
            state.cycle_used += pickup_dropoff_hrs
            phase_idx += 1
            continue

        if phase == "at_dropoff":
            loc, lat, lng = location_at(total_miles)
            _add_stop(state, "dropoff", loc, lat, lng, "Dropoff — unload freight (1 hr)")
            _add_segment(
                state,
                ON_DUTY,
                state.current_time,
                state.current_time + timedelta(hours=pickup_dropoff_hrs),
                loc,
                "Dropoff and unloading",
            )
            state.current_time += timedelta(hours=pickup_dropoff_hrs)
            state.cycle_used += pickup_dropoff_hrs
            phase_idx += 1
            continue

        # Driving phase
        while progress < target_progress - 0.1:
            if check_cycle():
                continue

            loc, lat, lng = location_at(progress)
            start_window(loc, lat, lng)

            if take_reset_if_needed(loc, lat, lng):
                continue

            take_break_if_needed(loc, lat, lng)
            fuel_if_needed(loc, lat, lng)

            remaining_drive_allowed = min(
                MAX_DRIVING_HRS - state.driving_in_window,
                BREAK_AFTER_DRIVING_HRS - state.driving_since_break,
                MAX_WINDOW_HRS - window_elapsed(),
            )
            if remaining_drive_allowed <= 0.05:
                take_reset_if_needed(loc, lat, lng)
                continue

            miles_left = target_progress - progress
            max_miles_this_stint = remaining_drive_allowed * speed
            chunk_miles = min(miles_left, max_miles_this_stint, fuel_interval - state.miles_since_fuel)

            if chunk_miles < 1:
                chunk_miles = min(miles_left, max_miles_this_stint)
            if chunk_miles < 0.1:
                take_reset_if_needed(loc, lat, lng)
                continue

            drive_hrs = chunk_miles / speed
            end_time = state.current_time + timedelta(hours=drive_hrs)
            end_loc, end_lat, end_lng = location_at(progress + chunk_miles)

            _add_segment(state, DRIVING, state.current_time, end_time, loc, "Driving", lat=lat, lng=lng, miles=chunk_miles)
            state.current_time = end_time
            progress += chunk_miles
            state.driving_in_window += drive_hrs
            state.driving_since_break += drive_hrs
            state.cycle_used += drive_hrs
            state.miles_since_fuel += chunk_miles
            state.miles_driven_today += chunk_miles
            day_key = state.current_time.date().isoformat()
            state.day_miles[day_key] = state.day_miles.get(day_key, 0) + chunk_miles

        phase_idx += 1

    # Post-trip at dropoff
    loc, lat, lng = location_at(total_miles)
    _add_segment(
        state,
        ON_DUTY,
        state.current_time,
        state.current_time + timedelta(hours=0.25),
        loc,
        "Post-trip inspection",
    )
    state.current_time += timedelta(hours=0.25)
    state.cycle_used += 0.25

    # 10-hour sleeper to end day
    _add_segment(
        state,
        SLEEPER,
        state.current_time,
        state.current_time + timedelta(hours=RESET_HRS),
        loc,
        "10-hour sleeper berth rest",
    )

    daily_logs = _build_daily_logs(state.segments, waypoints, route, state.day_miles)
    instructions = _build_instructions(state.stops, route)

    return {
        "segments": [_segment_to_dict(s) for s in state.segments if s.start >= start_time - timedelta(hours=1)],
        "stops": state.stops,
        "daily_logs": daily_logs,
        "instructions": instructions,
        "summary": {
            "total_miles": round(total_miles, 1),
            "driving_miles": round(sum(s.miles for s in state.segments if s.status == DRIVING), 1),
            "total_days": len(daily_logs),
            "cycle_used_end": round(state.cycle_used, 2),
            "estimated_completion": state.current_time.isoformat(),
        },
    }


def _take_reset(state: PlannerState, loc_info: tuple | tuple[str, float, float], reason: str):
    if isinstance(loc_info, tuple) and len(loc_info) == 3:
        loc, lat, lng = loc_info
    else:
        loc, lat, lng = loc_info[0], loc_info[1], loc_info[2]

    _add_stop(state, "rest", loc, lat, lng, f"10-hour reset — {reason}")
    _add_segment(
        state,
        SLEEPER,
        state.current_time,
        state.current_time + timedelta(hours=RESET_HRS),
        loc,
        f"10-hour sleeper berth ({reason})",
    )
    state.current_time += timedelta(hours=RESET_HRS)
    state.window_start = None
    state.driving_in_window = 0.0
    state.driving_since_break = 0.0


def _add_segment(
    state: PlannerState,
    status: str,
    start: datetime,
    end: datetime,
    location: str,
    remark: str = "",
    lat: float | None = None,
    lng: float | None = None,
    miles: float = 0.0,
):
    if end <= start:
        return
    state.segments.append(
        Segment(status=status, start=start, end=end, location=location, remark=remark, lat=lat, lng=lng, miles=miles)
    )


def _add_stop(state: PlannerState, kind: str, loc: str, lat: float, lng: float, description: str):
    state.stops.append(
        {
            "type": kind,
            "time": state.current_time.isoformat(),
            "location": loc,
            "lat": lat,
            "lng": lng,
            "description": description,
        }
    )


def _segment_to_dict(s: Segment) -> dict[str, Any]:
    return {
        "status": s.status,
        "start": s.start.isoformat(),
        "end": s.end.isoformat(),
        "location": s.location,
        "remark": s.remark,
        "lat": s.lat,
        "lng": s.lng,
        "miles": round(s.miles, 1),
        "duration_hours": round((s.end - s.start).total_seconds() / 3600, 2),
    }


def _build_daily_logs(
    segments: list[Segment],
    waypoints: list[dict],
    route: dict,
    day_miles: dict[str, float],
) -> list[dict[str, Any]]:
    trip_segments = [s for s in segments if s.remark != "10-hour off-duty reset before trip"]
    if not trip_segments:
        return []

    trip_start = min(s.start for s in trip_segments)
    first_day = trip_start.date()
    last_day = max(s.end.date() for s in trip_segments)
    all_days = []
    d = first_day
    while d <= last_day:
        all_days.append(d.isoformat())
        d += timedelta(days=1)

    priority = {DRIVING: 4, ON_DUTY: 3, SLEEPER: 2, OFF_DUTY: 1}
    logs = []
    for day in all_days:
        day_start = datetime.combine(datetime.fromisoformat(day).date(), datetime.min.time())
        if day_start.tzinfo is None and trip_segments[0].start.tzinfo:
            day_start = day_start.replace(tzinfo=trip_segments[0].start.tzinfo)
        day_end = day_start + timedelta(days=1)

        minutes = [OFF_DUTY] * (24 * 60)
        remarks = []

        for seg in trip_segments:
            if seg.end <= day_start or seg.start >= day_end:
                continue
            clip_start = max(seg.start, day_start)
            clip_end = min(seg.end, day_end)
            start_min = _minutes_from_midnight(clip_start)
            end_min = _minutes_from_midnight(clip_end)
            if clip_end.date() != clip_start.date():
                end_min = 24 * 60
            for m in range(start_min, min(end_min, 24 * 60)):
                if priority.get(seg.status, 0) >= priority.get(minutes[m], 0):
                    minutes[m] = seg.status
            if seg.remark and clip_start == seg.start:
                remarks.append(
                    {
                        "time": clip_start.strftime("%H:%M"),
                        "location": seg.location,
                        "text": seg.remark,
                    }
                )

        grid_segments = _minutes_to_segments(minutes)
        totals = {OFF_DUTY: 0.0, SLEEPER: 0.0, DRIVING: 0.0, ON_DUTY: 0.0}
        for seg in grid_segments:
            totals[seg["status"]] += (seg["end_minute"] - seg["start_minute"]) / 60

        dt = datetime.fromisoformat(day)
        logs.append(
            {
                "date": day,
                "date_display": dt.strftime("%B %d, %Y"),
                "month": dt.strftime("%m"),
                "day": dt.strftime("%d"),
                "year": dt.strftime("%Y"),
                "grid_segments": _merge_grid(grid_segments),
                "remarks": remarks,
                "totals": {k: round(v, 2) for k, v in totals.items()},
                "total_hours": round(sum(totals.values()), 2),
                "total_miles": round(day_miles.get(day, 0), 1),
                "route_from": waypoints[0].get("short_label") or waypoints[0]["label"],
                "route_to": waypoints[-1].get("short_label") or waypoints[-1]["label"],
                "carrier": "Example Carrier Inc.",
                "office_address": "123 Main St, Dallas, TX",
                "home_terminal": waypoints[0].get("short_label") or waypoints[0]["label"],
                "vehicle": "Unit 101 / Trailer 202",
                "shipping": "General freight",
                "recap": _build_recap(totals),
            }
        )
    return logs


def _minutes_to_segments(minutes: list[str]) -> list[dict]:
    if not minutes:
        return [{"status": OFF_DUTY, "start_minute": 0, "end_minute": 24 * 60}]
    segments = []
    current = minutes[0]
    start = 0
    for i in range(1, len(minutes)):
        if minutes[i] != current:
            segments.append({"status": current, "start_minute": start, "end_minute": i})
            current = minutes[i]
            start = i
    segments.append({"status": current, "start_minute": start, "end_minute": len(minutes)})
    return segments


def _merge_grid(segments: list[dict]) -> list[dict]:
    if not segments:
        return [{"status": OFF_DUTY, "start_minute": 0, "end_minute": 24 * 60}]
    segments = sorted(segments, key=lambda s: (s["start_minute"], s["status"]))
    return segments


def _minutes_from_midnight(dt: datetime) -> int:
    return dt.hour * 60 + dt.minute


def _build_recap(totals: dict[str, float]) -> dict[str, float]:
    on_duty_today = totals[DRIVING] + totals[ON_DUTY]
    return {
        "on_duty_today": round(on_duty_today, 2),
        "cycle_70hr_a": round(on_duty_today, 2),
        "cycle_70hr_b": round(70 - on_duty_today, 2),
        "cycle_70hr_c": round(on_duty_today, 2),
    }


def _build_instructions(stops: list[dict], route: dict) -> list[dict[str, str]]:
    instructions = []
    for i, leg in enumerate(route["legs"]):
        instructions.append(
            {
                "step": str(i + 1),
                "title": f"Drive: {leg['from']} → {leg['to']}",
                "detail": f"{leg['distance_miles']:.0f} mi · ~{leg['duration_hours']:.1f} hrs at highway speed",
            }
        )
    for stop in stops:
        instructions.append(
            {
                "step": "-",
                "title": stop["description"],
                "detail": f"{stop['location']} · {stop['time'][:16].replace('T', ' ')}",
            }
        )
    return instructions
