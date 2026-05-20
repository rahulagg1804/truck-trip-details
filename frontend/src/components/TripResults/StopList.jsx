import { STOP_META } from "../../constants/stops";
import { formatStopTime } from "../../utils/format";
import Icon from "../icons";

export default function StopList({ stops }) {
  return (
    <ul className="grid sm:grid-cols-2 gap-2 text-sm">
      {stops.map((stop) => {
        const meta = STOP_META[stop.type] || { label: stop.type, icon: "MapPin" };
        return (
          <li
            key={`${stop.type}-${stop.time}`}
            className="border border-slate-800 rounded-lg p-3 bg-slate-900 flex gap-3"
          >
            <span className="text-amber-500 mt-0.5">
              <Icon name={meta.icon} className="w-4 h-4" />
            </span>
            <div className="min-w-0">
              <p className="font-medium text-slate-200">
                {meta.label}: {stop.description}
              </p>
              <p className="text-slate-500 truncate">{stop.location}</p>
              <p className="text-xs text-slate-400 mt-1">{formatStopTime(stop.time)}</p>
            </div>
          </li>
        );
      })}
    </ul>
  );
}
