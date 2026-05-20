import Icon from "../icons";

const inputClass =
  "w-full pl-9 pr-3 py-2 rounded border border-slate-700 bg-slate-950 text-white placeholder:text-slate-600 focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500/40";

export default function FormField({
  name,
  label,
  icon,
  hint,
  type = "text",
  value,
  onChange,
  ...inputProps
}) {
  return (
    <label className="block">
      <span className="text-sm text-slate-300">{label}</span>
      <div className="relative mt-1">
        {icon && (
          <span className="pointer-events-none absolute left-2.5 top-1/2 -translate-y-1/2 text-slate-500">
            <Icon name={icon} className="w-4 h-4" />
          </span>
        )}
        <input
          name={name}
          type={type}
          value={value}
          onChange={onChange}
          className={inputClass}
          {...inputProps}
        />
      </div>
      {hint && <span className="mt-1 block text-xs text-slate-500">{hint}</span>}
    </label>
  );
}
