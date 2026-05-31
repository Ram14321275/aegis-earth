import { LayoutDashboard } from "lucide-react";
import { PageHeader } from "../../components/PageHeader";
import { useDocumentTitle } from "../../hooks/useDocumentTitle";
import { formatPageTitle } from "../../utils/format";

export function DashboardPage() {
  useDocumentTitle(formatPageTitle("Dashboard"));

  return (
    <section className="grid gap-6">
      <PageHeader
        eyebrow="Mission Overview"
        title="Dashboard"
        description="Application shell placeholder for the future MVP dashboard."
        icon={LayoutDashboard}
      />
      <div className="grid gap-4 md:grid-cols-3">
        <PlaceholderPanel title="Map Area" />
        <PlaceholderPanel title="Risk Summary" />
        <PlaceholderPanel title="Alert Queue" />
      </div>
    </section>
  );
}

function PlaceholderPanel({ title }: { title: string }) {
  return (
    <article className="min-h-44 rounded-lg border border-border bg-card p-5 shadow-aegis-panel">
      <p className="text-sm font-semibold text-foreground">{title}</p>
      <p className="mt-3 text-sm leading-6 text-muted">Reserved for Sprint 1 MVP implementation.</p>
    </article>
  );
}
