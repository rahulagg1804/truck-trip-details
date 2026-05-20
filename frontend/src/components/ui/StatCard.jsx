export default function StatCard({ label, value }) {
  return (
    <div className="border border-slate-800 rounded-lg p-3 bg-slate-900">
      <p className="text-slate-500 text-xs">{label}</p>
      <p className="text-lg font-semibold mt-0.5">{value}</p>
    </div>
  );
}
