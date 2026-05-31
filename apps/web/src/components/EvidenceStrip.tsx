import { Image, Layers3, SplitSquareHorizontal } from "lucide-react";
import type { EvidenceLayer } from "../types/intelligence";

type EvidenceStripProps = {
  layers: EvidenceLayer[];
};

const iconMap = {
  map: Image,
  heatmap: Layers3,
  difference: SplitSquareHorizontal,
};

export function EvidenceStrip({ layers }: EvidenceStripProps) {
  return (
    <div className="grid gap-3 md:grid-cols-3">
      {layers.map((layer) => {
        const Icon = iconMap[layer.type];
        return (
          <article key={layer.id} className="rounded-lg border border-border bg-card p-4 shadow-aegis-panel">
            <div className="flex items-center gap-2">
              <Icon className="h-5 w-5 text-primary" />
              <h3 className="font-semibold text-foreground">{layer.label}</h3>
            </div>
            <p className="mt-3 text-sm leading-6 text-muted">{layer.description}</p>
          </article>
        );
      })}
    </div>
  );
}

