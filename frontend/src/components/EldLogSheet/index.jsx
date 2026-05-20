import { useRef } from "react";
import { exportLogAsPng, exportLogAsPdf } from "../../utils/exportLog";
import Button from "../ui/Button";
import LogGrid from "./LogGrid";

export default function EldLogSheet({ log }) {
  const sheetRef = useRef(null);
  const totals = log.totals || {};
  const segments = log.grid_segments || [];

  async function handlePngExport() {
    await exportLogAsPng(sheetRef.current, `log-${log.date}.png`);
  }

  async function handlePdfExport() {
    await exportLogAsPdf(sheetRef.current, `log-${log.date}.pdf`);
  }

  return (
    <article className="space-y-2">
      <div className="flex justify-between items-center gap-2">
        <h4 className="text-white font-medium">{log.date_display}</h4>
        <div className="flex gap-2">
          <Button variant="secondary" onClick={handlePngExport}>
            PNG
          </Button>
          <Button variant="secondary" onClick={handlePdfExport}>
            PDF
          </Button>
        </div>
      </div>

      <div
        ref={sheetRef}
        className="bg-white text-black text-[10px] border border-slate-400"
        style={{ fontFamily: "Arial, sans-serif" }}
      >
        <header className="border-b border-slate-400 p-2 grid grid-cols-2 gap-2">
          <div>
            <p className="font-bold text-[11px]">DRIVER&apos;S DAILY LOG</p>
            <p className="text-[8px] text-slate-600">24 hour period</p>
          </div>
          <div className="text-right">
            <p>
              Date: {log.month}/{log.day}/{log.year}
            </p>
            <p>Miles: {log.total_miles}</p>
          </div>
          <p>Route: {log.route_from} to {log.route_to}</p>
          <p>Carrier: {log.carrier}</p>
          <p>{log.office_address}</p>
          <p>{log.vehicle}</p>
        </header>

        <LogGrid segments={segments} totals={totals} />

        <section className="border-t border-slate-400 p-2">
          <p className="font-bold text-[9px]">REMARKS</p>
          <ul>
            {log.remarks?.map((remark) => (
              <li key={`${remark.time}-${remark.location}`} className="text-[9px]">
                {remark.time} {remark.location} — {remark.text}
              </li>
            ))}
          </ul>
          <p className="text-[8px] mt-1">{log.shipping}</p>
        </section>

        <footer className="border-t border-slate-400 p-2 grid grid-cols-4 gap-1 text-[8px] bg-slate-50">
          <span>On duty today: {log.recap?.on_duty_today}</span>
          <span>70hr (A): {log.recap?.cycle_70hr_a}</span>
          <span>Avail (B): {log.recap?.cycle_70hr_b}</span>
          <span>8-day (C): {log.recap?.cycle_70hr_c}</span>
        </footer>
      </div>
    </article>
  );
}
