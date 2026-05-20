export default function InstructionsList({ instructions }) {
  return (
    <ol className="space-y-2 text-sm">
      {instructions.map((item, index) => (
        <li key={`${item.step}-${index}`} className="flex gap-2">
          <span className="text-slate-500 w-5 shrink-0 font-mono text-xs">{item.step}</span>
          <div>
            <p className="text-slate-200">{item.title}</p>
            <p className="text-slate-500 text-xs">{item.detail}</p>
          </div>
        </li>
      ))}
    </ol>
  );
}
