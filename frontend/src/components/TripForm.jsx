import { useState } from "react";
import { TRIP_FORM_FIELDS } from "../constants/trip";
import FormField from "./ui/FormField";
import Button from "./ui/Button";

export default function TripForm({ initial, loading, onSubmit }) {
  const [form, setForm] = useState(initial);

  function handleChange(e) {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  }

  function handleSubmit(e) {
    e.preventDefault();
    onSubmit({
      ...form,
      current_cycle_used: parseFloat(form.current_cycle_used) || 0,
    });
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="space-y-4 p-5 rounded-lg border border-slate-800 bg-slate-900"
    >
      <div className="grid sm:grid-cols-2 gap-4">
        {TRIP_FORM_FIELDS.map((field) => (
          <FormField
            key={field.name}
            name={field.name}
            label={field.label}
            icon={field.icon}
            hint={field.hint}
            type={field.type}
            placeholder={field.placeholder}
            min={field.min}
            max={field.max}
            step={field.step}
            value={form[field.name]}
            onChange={handleChange}
            required={field.type !== "number"}
          />
        ))}
      </div>

      <Button type="submit" loading={loading} variant="primary">
        {loading ? "Planning…" : "Plan trip"}
      </Button>
    </form>
  );
}
