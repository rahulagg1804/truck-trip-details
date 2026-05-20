import Icon from "../icons";

export default function Button({
  children,
  loading = false,
  variant = "primary",
  type = "button",
  className = "",
  ...props
}) {
  const variants = {
    primary: "bg-amber-500 text-slate-950 hover:bg-amber-400",
    secondary: "border border-slate-600 text-slate-200 hover:border-slate-500",
  };

  return (
    <button
      type={type}
      disabled={loading || props.disabled}
      className={`inline-flex items-center justify-center gap-2 px-4 py-2 rounded font-medium text-sm disabled:opacity-50 disabled:cursor-not-allowed transition-colors ${variants[variant]} ${className}`}
      {...props}
    >
      {loading && <Icon name="Loader2" className="w-4 h-4 animate-spin" />}
      {children}
    </button>
  );
}
