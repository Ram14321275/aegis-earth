import { motion } from "framer-motion";
import { ArrowRight, Globe2, Radar } from "lucide-react";
import { Link } from "react-router-dom";
import { Button } from "../../components/ui/button";
import { useDocumentTitle } from "../../hooks/useDocumentTitle";
import { formatPageTitle } from "../../utils/format";

export function HomePage() {
  useDocumentTitle(formatPageTitle("Home"));

  return (
    <section className="grid min-h-[calc(100vh-112px)] gap-8 py-8 lg:grid-cols-[1fr_420px] lg:items-center">
      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.42 }}
        className="max-w-3xl"
      >
        <p className="font-mono text-sm uppercase tracking-[0.28em] text-signal">Earth Intelligence Platform</p>
        <h1 className="mt-5 text-5xl font-bold tracking-normal text-foreground sm:text-6xl lg:text-7xl">
          Aegis Earth
        </h1>
        <p className="mt-5 text-2xl font-semibold text-primary">Observe. Analyze. Protect.</p>
        <p className="mt-6 max-w-2xl text-lg leading-8 text-muted">
          A dark mission-control shell for the Sprint 1 MVP. Routing, layout, and navigation are ready for the
          disaster intelligence workflows that follow.
        </p>
        <div className="mt-8 flex flex-wrap gap-3">
          <Button asChild>
            <Link to="/dashboard">
              Open Dashboard
              <ArrowRight className="h-4 w-4" aria-hidden="true" />
            </Link>
          </Button>
          <Button asChild variant="secondary">
            <Link to="/analysis">Analysis Workspace</Link>
          </Button>
        </div>
      </motion.div>

      <motion.aside
        initial={{ opacity: 0, scale: 0.97 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.45, delay: 0.08 }}
        className="rounded-lg border border-border bg-card p-5 shadow-aegis-panel backdrop-blur-xl"
      >
        <div className="flex items-center gap-3 border-b border-border pb-4">
          <Radar className="h-6 w-6 text-primary" aria-hidden="true" />
          <div>
            <h2 className="font-bold text-foreground">Navigation Shell</h2>
            <p className="text-sm text-muted">Future-ready application structure</p>
          </div>
        </div>
        <div className="mt-5 grid gap-3">
          <StatusRow label="Responsive Layout" value="Ready" />
          <StatusRow label="React Router" value="Ready" />
          <StatusRow label="Dark Theme" value="Ready" />
          <StatusRow label="Disaster Logic" value="Deferred" />
        </div>
        <div className="mt-5 rounded-md border border-border bg-white/[0.03] p-4">
          <Globe2 className="h-5 w-5 text-signal" aria-hidden="true" />
          <p className="mt-3 text-sm leading-6 text-muted">
            Checkpoint 4 focuses on application architecture only. API integration and hazard workflows remain
            intentionally deferred.
          </p>
        </div>
      </motion.aside>
    </section>
  );
}

function StatusRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between rounded-md border border-border bg-white/[0.03] px-4 py-3">
      <span className="text-sm text-muted">{label}</span>
      <span className="text-sm font-semibold text-foreground">{value}</span>
    </div>
  );
}
