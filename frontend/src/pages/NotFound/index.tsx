import { Link } from "react-router-dom";
import { Button } from "../../components/ui/button";
import { useDocumentTitle } from "../../hooks/useDocumentTitle";
import { formatPageTitle } from "../../utils/format";

export function NotFoundPage() {
  useDocumentTitle(formatPageTitle("Not Found"));

  return (
    <section className="grid min-h-[calc(100vh-160px)] place-items-center">
      <div className="max-w-md rounded-lg border border-border bg-card p-6 text-center shadow-aegis-panel">
        <p className="font-mono text-sm uppercase tracking-[0.24em] text-signal">404</p>
        <h1 className="mt-3 text-3xl font-bold text-foreground">Page Not Found</h1>
        <p className="mt-3 text-sm leading-6 text-muted">The requested Aegis Earth route does not exist.</p>
        <Button asChild className="mt-6">
          <Link to="/">Return Home</Link>
        </Button>
      </div>
    </section>
  );
}
