import { FormEvent, useState } from "react";
import { Loader2, LocateFixed, Search } from "lucide-react";
import { Button } from "./ui/button";

type SearchConsoleProps = {
  isLoading: boolean;
  onAnalyze: (query: string) => void;
};

export function SearchConsole({ isLoading, onAnalyze }: SearchConsoleProps) {
  const [query, setQuery] = useState("Hyderabad");

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    onAnalyze(query);
  }

  return (
    <form onSubmit={handleSubmit} className="grid gap-3">
      <label htmlFor="location-search" className="text-xs font-semibold uppercase tracking-[0.16em] text-muted">
        Location Intelligence
      </label>
      <div className="flex flex-col gap-2 sm:flex-row">
        <div className="relative flex-1">
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted" />
          <input
            id="location-search"
            className="h-11 w-full rounded-md border border-border bg-slate-950/70 pl-10 pr-3 text-sm text-foreground outline-none transition placeholder:text-muted focus:border-primary focus:ring-2 focus:ring-primary/20"
            placeholder="City or coordinates, e.g. 17.3850,78.4867"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
          />
        </div>
        <Button type="submit" disabled={isLoading || !query.trim()}>
          {isLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : <LocateFixed className="h-4 w-4" />}
          Analyze
        </Button>
      </div>
    </form>
  );
}

