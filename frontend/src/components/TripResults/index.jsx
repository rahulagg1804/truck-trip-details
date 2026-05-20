import Icon from "../icons";
import Card from "../ui/Card";
import StatCard from "../ui/StatCard";
import RouteMap from "../RouteMap";
import EldLogSheet from "../EldLogSheet";
import StopList from "./StopList";
import InstructionsList from "./InstructionsList";

export default function TripResults({ data }) {
  const { route, plan, inputs } = data;
  const { summary } = plan;
  const routeLabel = [inputs.current_location, inputs.pickup_location, inputs.dropoff_location].join(
    " → "
  );

  return (
    <section className="space-y-8">
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <StatCard label="Distance" value={`${summary.total_miles} mi`} />
        <StatCard label="Driving" value={`${summary.driving_miles} mi`} />
        <StatCard label="Log days" value={summary.total_days} />
        <StatCard label="Cycle end" value={`${summary.cycle_used_end} h`} />
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        <Card title="Route" subtitle={routeLabel} className="overflow-hidden">
          <RouteMap route={route} stops={plan.stops} />
        </Card>

        <Card title="Instructions" className="p-4 max-h-96 overflow-y-auto">
          <InstructionsList instructions={plan.instructions} />
        </Card>
      </div>

      <section>
        <h3 className="font-medium mb-2 flex items-center gap-2">
          <Icon name="Route" className="w-4 h-4 text-amber-500" />
          Stops
        </h3>
        <StopList stops={plan.stops} />
      </section>

      <section>
        <h3 className="font-medium mb-4 flex items-center gap-2">
          <Icon name="FileText" className="w-4 h-4 text-amber-500" />
          Daily logs
          {plan.daily_logs.length > 1 && (
            <span className="text-slate-500 text-sm font-normal">
              ({plan.daily_logs.length} days)
            </span>
          )}
        </h3>
        <div className="space-y-8">
          {plan.daily_logs.map((log) => (
            <EldLogSheet key={log.date} log={log} />
          ))}
        </div>
      </section>
    </section>
  );
}
