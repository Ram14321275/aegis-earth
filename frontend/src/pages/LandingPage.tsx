import { motion } from "framer-motion";
import { Activity, Globe2, Map } from "lucide-react";
import { BrandMark } from "../components/BrandMark";
import { Button } from "../components/ui/button";

const signals = [
  { label: "Flood Detection", icon: Map },
  { label: "Wildfire Detection", icon: Activity },
  { label: "Satellite Analysis", icon: Globe2 },
];

export function LandingPage() {
  return (
    <main className="min-h-screen overflow-hidden bg-background text-foreground">
      <section className="mx-auto flex min-h-screen w-full max-w-7xl flex-col justify-between px-6 py-6">
        <nav className="flex items-center justify-between">
          <BrandMark />
          <Button variant="secondary" type="button">
            Mission Console
          </Button>
        </nav>

        <div className="grid gap-10 py-16 lg:grid-cols-[1fr_420px] lg:items-center">
          <motion.div
            initial={{ opacity: 0, y: 18 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.45 }}
            className="max-w-3xl"
          >
            <p className="font-mono text-sm uppercase tracking-[0.28em] text-signal">
              Earth Intelligence Platform
            </p>
            <h1 className="mt-5 text-5xl font-bold tracking-normal text-foreground sm:text-6xl lg:text-7xl">
              Aegis Earth
            </h1>
            <p className="mt-5 text-2xl font-semibold text-primary">Observe. Analyze. Protect.</p>
            <p className="mt-6 max-w-2xl text-lg leading-8 text-muted">
              A dark mission-control foundation for flood and wildfire intelligence, built for visual evidence,
              explainable risk, and resilient disaster response workflows.
            </p>
          </motion.div>

          <motion.aside
            initial={{ opacity: 0, scale: 0.96 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="rounded-lg border border-border bg-card p-5 shadow-aegis-panel backdrop-blur-xl"
          >
            <div className="grid gap-3">
              {signals.map((signal) => {
                const Icon = signal.icon;
                return (
                  <div key={signal.label} className="flex items-center gap-3 rounded-md border border-border bg-white/[0.03] p-4">
                    <Icon className="h-5 w-5 text-primary" aria-hidden="true" />
                    <span className="font-semibold text-foreground">{signal.label}</span>
                  </div>
                );
              })}
            </div>
          </motion.aside>
        </div>

        <footer className="border-t border-border pt-5 text-sm text-muted">
          Sprint 1 MVP foundation: React, Vite, TypeScript, Tailwind CSS, shadcn/ui, Framer Motion, Leaflet.
        </footer>
      </section>
    </main>
  );
}

