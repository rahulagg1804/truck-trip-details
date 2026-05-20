import Icon from "../icons";

export default function Alert({ children }) {
  if (!children) return null;
  return (
    <div
      role="alert"
      className="mt-3 flex gap-2 text-sm text-red-300 border border-red-900 bg-red-950/50 rounded px-3 py-2"
    >
      <Icon name="AlertCircle" className="w-4 h-4 shrink-0 mt-0.5" />
      <span>{children}</span>
    </div>
  );
}
