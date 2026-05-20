import { DEFAULT_TRIP } from "./constants/trip";
import { usePlanTrip } from "./hooks/usePlanTrip";
import AppHeader from "./components/layout/AppHeader";
import TripForm from "./components/TripForm";
import TripResults from "./components/TripResults";
import Alert from "./components/ui/Alert";

export default function App() {
  const { loading, error, result, submit } = usePlanTrip();

  return (
    <div className="min-h-screen">
      <AppHeader />

      <main className="max-w-6xl mx-auto px-4 py-8 space-y-8">
        <section>
          <h2 className="text-xl font-semibold mb-1">Trip details</h2>
          <p className="text-slate-400 text-sm mb-4">
            Locations and hours already used in your 8-day cycle.
          </p>
          <TripForm initial={DEFAULT_TRIP} loading={loading} onSubmit={submit} />
          <Alert>{error}</Alert>
        </section>

        {result && <TripResults data={result} />}
      </main>
    </div>
  );
}
