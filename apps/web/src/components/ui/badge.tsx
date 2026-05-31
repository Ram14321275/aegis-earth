import type { ReactNode } from "react";
import { cn } from "../../lib/utils";
import type { RiskBand } from "../../types/intelligence";

const riskClass: Record<RiskBand, string> = {
  low: "border-emerald-300/40 bg-emerald-400/10 text-emerald-200",
  moderate: "border-sky-300/40 bg-sky-400/10 text-sky-100",
  high: "border-warning/50 bg-warning/10 text-warning",
  critical: "border-danger/50 bg-danger/10 text-danger",
};

type BadgeProps = {
  children: ReactNode;
  risk?: RiskBand;
  className?: string;
};

export function Badge({ children, risk, className }: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-md border px-2 py-1 text-xs font-semibold uppercase tracking-[0.08em]",
        risk ? riskClass[risk] : "border-border bg-white/5 text-muted",
        className,
      )}
    >
      {children}
    </span>
  );
}
