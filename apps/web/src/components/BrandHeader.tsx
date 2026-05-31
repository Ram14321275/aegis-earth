import { Activity, Radar, ShieldCheck } from "lucide-react";
import { Badge } from "./ui/badge";

export function BrandHeader() {
  return (
    <header className="flex flex-col gap-4 border-b border-border bg-background/90 px-5 py-4 backdrop-blur-xl lg:flex-row lg:items-center lg:justify-between">
      <div className="flex items-center gap-3">
        <div className="grid h-11 w-11 place-items-center rounded-md border border-primary/40 bg-primary/10">
          <ShieldCheck className="h-6 w-6 text-primary" aria-hidden="true" />
        </div>
        <div>
          <h1 className="text-xl font-bold tracking-normal text-foreground">Aegis Earth</h1>
          <p className="text-sm text-muted">Observe. Analyze. Protect.</p>
        </div>
      </div>
      <div className="flex flex-wrap items-center gap-2">
        <Badge>Mission Control</Badge>
        <Badge>Sentinel Ready</Badge>
        <span className="inline-flex items-center gap-2 rounded-md border border-border bg-white/5 px-3 py-2 text-xs text-muted">
          <Activity className="h-4 w-4 text-primary" aria-hidden="true" />
          MVP Sprint 1
        </span>
        <span className="inline-flex items-center gap-2 rounded-md border border-border bg-white/5 px-3 py-2 text-xs text-muted">
          <Radar className="h-4 w-4 text-signal" aria-hidden="true" />
          Flood + Wildfire
        </span>
      </div>
    </header>
  );
}

