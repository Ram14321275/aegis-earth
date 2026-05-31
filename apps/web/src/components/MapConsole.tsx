import { useEffect, useRef } from "react";
import type { ElementType } from "react";
import { Layers, Map, ScanLine } from "lucide-react";
import type { Map as LeafletMap } from "leaflet";
import type { Coordinates, LayerMode } from "../types/intelligence";
import { Button } from "./ui/button";

type MapConsoleProps = {
  coordinates: Coordinates;
  mode: LayerMode;
  onModeChange: (mode: LayerMode) => void;
};

const modes: Array<{ id: LayerMode; label: string; icon: ElementType }> = [
  { id: "map", label: "Map", icon: Map },
  { id: "heatmap", label: "Heat", icon: Layers },
  { id: "difference", label: "Diff", icon: ScanLine },
];

export function MapConsole({ coordinates, mode, onModeChange }: MapConsoleProps) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const mapRef = useRef<LeafletMap | null>(null);
  const markerRef = useRef<import("leaflet").CircleMarker | null>(null);
  const overlayRef = useRef<import("leaflet").Circle | null>(null);

  useEffect(() => {
    let disposed = false;

    async function setupMap() {
      if (!containerRef.current || mapRef.current) return;
      const L = await import("leaflet");
      if (disposed || !containerRef.current) return;

      const map = L.map(containerRef.current, {
        zoomControl: false,
        attributionControl: false,
      }).setView([coordinates.latitude, coordinates.longitude], 11);

      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 18,
      }).addTo(map);

      L.control.zoom({ position: "bottomright" }).addTo(map);
      mapRef.current = map;
    }

    setupMap();

    return () => {
      disposed = true;
    };
  }, [coordinates.latitude, coordinates.longitude]);

  useEffect(() => {
    async function updateMap() {
      if (!mapRef.current) return;
      const L = await import("leaflet");
      const center: [number, number] = [coordinates.latitude, coordinates.longitude];
      mapRef.current.setView(center, 11, { animate: true });

      markerRef.current?.remove();
      overlayRef.current?.remove();

      const color = mode === "difference" ? "#ff6b6b" : mode === "heatmap" ? "#f2b84b" : "#49d3b4";

      overlayRef.current = L.circle(center, {
        radius: mode === "map" ? 2600 : 6200,
        color,
        fillColor: color,
        fillOpacity: mode === "map" ? 0.12 : 0.28,
        weight: 1.5,
      }).addTo(mapRef.current);

      markerRef.current = L.circleMarker(center, {
        radius: 7,
        color: "#e7eef8",
        fillColor: color,
        fillOpacity: 1,
        weight: 2,
      }).addTo(mapRef.current);
    }

    updateMap();
  }, [coordinates, mode]);

  return (
    <div className="relative min-h-[420px] overflow-hidden rounded-lg border border-border bg-slate-950">
      <div ref={containerRef} className="absolute inset-0 z-0" aria-label="Aegis Earth map view" />
      <div className={`map-overlay map-overlay-${mode}`} />
      <div className="absolute left-4 top-4 z-[500] flex gap-2 rounded-md border border-border bg-background/80 p-1 backdrop-blur-xl">
        {modes.map((item) => {
          const Icon = item.icon;
          return (
            <Button
              key={item.id}
              type="button"
              variant={mode === item.id ? "primary" : "ghost"}
              size="default"
              onClick={() => onModeChange(item.id)}
              title={`${item.label} view`}
            >
              <Icon className="h-4 w-4" />
              {item.label}
            </Button>
          );
        })}
      </div>
      <div className="absolute bottom-4 left-4 z-[500] rounded-md border border-border bg-background/85 px-3 py-2 font-mono text-xs text-muted backdrop-blur-xl">
        {coordinates.latitude.toFixed(4)}, {coordinates.longitude.toFixed(4)}
      </div>
    </div>
  );
}
