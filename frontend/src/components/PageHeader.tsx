import type { ElementType } from "react";

type PageHeaderProps = {
  eyebrow: string;
  title: string;
  description: string;
  icon: ElementType;
};

export function PageHeader({ eyebrow, title, description, icon: Icon }: PageHeaderProps) {
  return (
    <header className="rounded-lg border border-border bg-card p-5 shadow-aegis-panel">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center">
        <div className="grid h-12 w-12 place-items-center rounded-lg border border-primary/40 bg-primary/10">
          <Icon className="h-6 w-6 text-primary" aria-hidden="true" />
        </div>
        <div>
          <p className="font-mono text-xs uppercase tracking-[0.22em] text-signal">{eyebrow}</p>
          <h1 className="mt-1 text-3xl font-bold text-foreground">{title}</h1>
          <p className="mt-2 max-w-2xl text-sm leading-6 text-muted">{description}</p>
        </div>
      </div>
    </header>
  );
}
