import { DUTY_ROWS, GRID, HOUR_TICKS, minuteToX, hourLabel } from "../../constants/eldLog";

export default function LogGrid({ segments, totals }) {
  const viewHeight = DUTY_ROWS.length * GRID.rowHeight + 40;

  return (
    <svg
      viewBox={`0 0 ${GRID.left + GRID.width + 60} ${viewHeight}`}
      className="w-full block"
    >
      {HOUR_TICKS.map((h) => (
        <text
          key={h}
          x={minuteToX(h * 60)}
          y={12}
          textAnchor="middle"
          fontSize="8"
          fill="#64748b"
        >
          {hourLabel(h)}
        </text>
      ))}

      {DUTY_ROWS.map((row, rowIndex) => {
        const y = 20 + rowIndex * GRID.rowHeight;
        const rowSegments = segments.filter((s) => s.status === row.key);

        return (
          <g key={row.key}>
            <text x={4} y={y + GRID.rowHeight / 2 + 3} fontSize="8" fontWeight="600">
              {row.label}
            </text>
            <rect
              x={GRID.left}
              y={y}
              width={GRID.width}
              height={GRID.rowHeight - 2}
              fill="#f8fafc"
              stroke="#cbd5e1"
            />
            {Array.from({ length: 24 }).map((_, i) => (
              <line
                key={i}
                x1={GRID.left + (i / 24) * GRID.width}
                y1={y}
                x2={GRID.left + (i / 24) * GRID.width}
                y2={y + GRID.rowHeight - 2}
                stroke="#e2e8f0"
                strokeWidth="0.5"
              />
            ))}
            {rowSegments.map((seg, i) => (
              <line
                key={i}
                x1={minuteToX(seg.start_minute)}
                y1={y + GRID.rowHeight / 2}
                x2={minuteToX(seg.end_minute)}
                y2={y + GRID.rowHeight / 2}
                stroke={row.color}
                strokeWidth="2.5"
              />
            ))}
            <text
              x={GRID.left + GRID.width + 6}
              y={y + GRID.rowHeight / 2 + 3}
              fontSize="9"
              fontWeight="700"
            >
              {(totals[row.key] || 0).toFixed(2)}
            </text>
          </g>
        );
      })}
    </svg>
  );
}
