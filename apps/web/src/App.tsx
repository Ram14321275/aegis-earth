import { useState } from "react";
import { motion } from "framer-motion";
import { analyzeLocation, getDemoResult } from "./api/intelligence";
import { BrandHeader } from "./components/BrandHeader";
import { EvidenceStrip } from "./components/EvidenceStrip";
import { ExplainabilityPanel } from "./components/ExplainabilityPanel";
import { MapConsole } from "./components/MapConsole";
import { RiskPanel } from "./components/RiskPanel";
import { SearchConsole } from "./components/SearchConsole";
import { Panel } from "./components/ui/panel";
import type { IntelligenceResult, LayerMode } from "./types/intelligence";

export function App() {
  const [result, setResult] = useState<IntelligenceResult>(() => getDemoResult());
  const [layerMode, setLayerMode] = useState<LayerMode>("map");
  const [isLoading, setIsLoading] = useState(false);
  const [status, setStatus] = useState("Demo intelligence loaded. Connect backend for live Sprint 1 API responses.");

  async function handleAnalyze(query: string) {
    setIsLoading(true);
    setStatus("Resolving search and requesting disaster intelligence...");
    try {
      const nextResult = await analyzeLocation(query);
      setResult(nextResult);
      setStatus("Analysis complete.");
    } catch (error) {
      setStatus(error instanceof Error ? `${error.message}. Showing local demo result.` : "Analysis failed.");
      setResult(getDemoResult());
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-background text-foreground">
      <BrandHeader />
      <div className="mx-auto grid w-full max-w-[1600px] gap-4 px-4 py-4">
        <Panel>
          <SearchConsole isLoading={isLoading} onAnalyze={handleAnalyze} />
          <p className="mt-3 text-sm text-muted">{status}</p>
        </Panel>

        <motion.section
          className="grid gap-4 xl:grid-cols-[1fr_380px]"
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.35 }}
        >
          <MapConsole coordinates={result.coordinates} mode={layerMode} onModeChange={setLayerMode} />
          <RiskPanel result={result} />
        </motion.section>

        <section className="grid gap-4 xl:grid-cols-[1fr_420px]">
          <EvidenceStrip layers={result.evidenceLayers} />
          <ExplainabilityPanel result={result} />
        </section>
      </div>
    </main>
  );
}

