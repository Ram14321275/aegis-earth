import { AlertTriangle, Flame, Waves } from "lucide-react";
import type { IntelligenceResult } from "../types/intelligence";
import { Badge } from "./ui/badge";
import { Panel } from "./ui/panel";

type RiskPanelProps = {
  result: IntelligenceResult;
};

const signalIcon = {
  flood: Waves,
  wildfire: Flame,
};

export function RiskPanel({ result }: RiskPanelProps) {
  return (
    <Panel className="grid gap-4">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-muted">Risk Assessment</p>
          <h2 className="mt-1 text-2xl font-bold text-foreground">{result.locationName}</h2>
        </div>
        <Badge risk={result.overallRisk}>{result.overallRisk}</Badge>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <Metric label="Confidence" value={`${Math.round(result.confidence * 100)}%`} />
        <Metric label="Signals" value={String(result.signals.length)} />
      </div>

      <div className="grid gap-3">
        {result.signals.map((signal) => {
          const Icon = signalIcon[signal.type];
          return (
            <article key={signal.type} className="rounded-md border border-border bg-white/[0.03] p-3">
              <div className="flex items-center justify-between gap-2">
                <div className="flex items-center gap-2 text-sm font-semibold capitalize text-foreground">
                  <Icon className="h-4 w-4 text-primary" />
                  {signal.type}
                </div>
                <Badge risk={signal.risk}>{Math.round(signal.confidence * 100)}%</Badge>
              </div>
              <ul className="mt-3 grid gap-2 text-sm text-muted">
                {signal.drivers.map((driver) => (
                  <li key={driver} className="flex gap-2">
                    <AlertTriangle className="mt-0.5 h-3.5 w-3.5 shrink-0 text-warning" />
                    <span>{driver}</span>
                  </li>
                ))}
              </ul>
            </article>
          );
        })}
      </div>
    </Panel>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-md border border-border bg-slate-950/50 p-3">
      <p className="text-xs uppercase tracking-[0.14em] text-muted">{label}</p>
      <p className="mt-1 text-xl font-bold text-foreground">{value}</p>
    </div>
  );
}

