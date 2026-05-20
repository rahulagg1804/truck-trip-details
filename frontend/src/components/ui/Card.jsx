export default function Card({ title, subtitle, children, className = "" }) {
  return (
    <div className={`border border-slate-800 rounded-lg bg-slate-900 ${className}`}>
      {(title || subtitle) && (
        <div className="px-4 py-2 border-b border-slate-800">
          {title && <div className="font-medium text-sm">{title}</div>}
          {subtitle && <div className="text-slate-400 text-xs mt-0.5">{subtitle}</div>}
        </div>
      )}
      {children}
    </div>
  );
}
