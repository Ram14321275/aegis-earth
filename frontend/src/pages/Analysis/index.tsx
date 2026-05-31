import { Activity } from "lucide-react";
import { PageHeader } from "../../components/PageHeader";
import { useDocumentTitle } from "../../hooks/useDocumentTitle";
import { formatPageTitle } from "../../utils/format";

export function AnalysisPage() {
  useDocumentTitle(formatPageTitle("Analysis"));

  return (
    <section className="grid gap-6">
      <PageHeader
        eyebrow="Evidence Workspace"
        title="Analysis"
        description="Routing destination prepared for future satellite evidence and explainability workflows."
        icon={Activity}
      />
      <div className="rounded-lg border border-border bg-card p-5 shadow-aegis-panel">
        <div className="aspect-[16/7] rounded-md border border-dashed border-border bg-slate-950/55" />
      </div>
    </section>
  );
}
