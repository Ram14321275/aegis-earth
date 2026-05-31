import type { ReactNode } from "react";
import { cn } from "../../lib/utils";

type PanelProps = {
  children: ReactNode;
  className?: string;
};

export function Panel({ children, className }: PanelProps) {
  return (
    <section
      className={cn(
        "rounded-lg border border-border bg-card p-4 shadow-aegis-panel backdrop-blur-xl",
        className,
      )}
    >
      {children}
    </section>
  );
}
