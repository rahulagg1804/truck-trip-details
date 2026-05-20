import Icon from "../icons";

export default function AppHeader() {
  return (
    <header className="border-b border-slate-800 bg-slate-900">
      <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Icon name="Truck" className="w-5 h-5 text-amber-500" />
          <h1 className="text-lg font-semibold">Truck Trip Planner</h1>
        </div>
        <span className="text-xs text-slate-400 border border-slate-700 rounded px-2 py-0.5">
          70hr / 8-day
        </span>
      </div>
    </header>
  );
}
