import { BrainCircuit, Siren } from "lucide-react";
import type { IntelligenceResult } from "../types/intelligence";
import { Badge } from "./ui/badge";
import { Panel } from "./ui/panel";

type ExplainabilityPanelProps = {
  result: IntelligenceResult;
};

export function ExplainabilityPanel({ result }: ExplainabilityPanelProps) {
  return (
    <Panel className="grid gap-4">
      <div className="flex items-center gap-2">
        <BrainCircuit className="h-5 w-5 text-primary" />
        <h2 className="text-lg font-bold text-foreground">Why This Area Is Dangerous</h2>
      </div>

      <div className="grid gap-3">
        {result.explanation.map((item) => (
          <p key={item} className="rounded-md border border-border bg-white/[0.03] p-3 text-sm leading-6 text-muted">
            {item}
          </p>
        ))}
      </div>

      <div className="grid gap-2">
        <p className="text-xs font-semibold uppercase tracking-[0.16em] text-muted">Generated Alerts</p>
        {result.alerts.map((alert) => (
          <article key={alert.id} className="rounded-md border border-warning/35 bg-warning/10 p-3">
            <div className="flex items-center justify-between gap-3">
              <div className="flex items-center gap-2 text-sm font-semibold text-foreground">
                <Siren className="h-4 w-4 text-warning" />
                {alert.title}
              </div>
              <Badge risk={alert.severity}>{alert.severity}</Badge>
            </div>
            <p className="mt-2 text-sm text-muted">{alert.message}</p>
          </article>
        ))}
      </div>
    </Panel>
  );
}

