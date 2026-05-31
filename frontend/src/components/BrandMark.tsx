import { ShieldCheck } from "lucide-react";

export function BrandMark() {
  return (
    <div className="flex items-center gap-3">
      <div className="grid h-12 w-12 place-items-center rounded-lg border border-primary/40 bg-primary/10 shadow-aegis-panel">
        <ShieldCheck className="h-7 w-7 text-primary" aria-hidden="true" />
      </div>
      <div>
        <p className="text-sm font-semibold uppercase tracking-[0.22em] text-primary">Disaster Intelligence</p>
        <p className="text-sm text-muted">Sprint 1 Frontend</p>
      </div>
    </div>
  );
}

