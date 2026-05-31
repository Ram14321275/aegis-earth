import type { IntelligenceResult } from "../types/intelligence";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

const fallbackResult: IntelligenceResult = {
  locationName: "Hyderabad",
  coordinates: { latitude: 17.385, longitude: 78.4867 },
  generatedAt: new Date().toISOString(),
  overallRisk: "high",
  confidence: 0.82,
  signals: [
    {
      type: "flood",
      risk: "high",
      confidence: 0.84,
      drivers: ["Low-lying urban catchments", "Recent rainfall anomaly", "Dense impervious surface"],
    },
    {
      type: "wildfire",
      risk: "moderate",
      confidence: 0.68,
      drivers: ["Elevated surface temperature", "Dry vegetation pockets", "Moderate wind exposure"],
    },
  ],
  evidenceLayers: [
    {
      id: "base-map",
      label: "Operational Map",
      type: "map",
      description: "Coordinate resolved base layer with terrain and urban context.",
    },
    {
      id: "risk-heat",
      label: "Risk Heat Map",
      type: "heatmap",
      description: "Composite hazard intensity surface from flood and wildfire indicators.",
    },
    {
      id: "change-diff",
      label: "Difference Map",
      type: "difference",
      description: "Before vs after evidence layer reserved for Sentinel analysis outputs.",
    },
  ],
  alerts: [
    {
      id: "alert-1",
      severity: "high",
      title: "Flood watch recommended",
      message: "Hydrology indicators suggest elevated flood exposure around the selected area.",
    },
  ],
  explanation: [
    "The flood score is driven by urban runoff exposure, low elevation sensitivity, and rainfall anomaly indicators.",
    "Wildfire risk remains below flood risk because vegetation dryness is localized rather than regional.",
    "Confidence reflects available open weather inputs and placeholder satellite provider status for Sprint 1.",
  ],
};

export async function analyzeLocation(query: string): Promise<IntelligenceResult> {
  const response = await fetch(`${API_BASE_URL}/api/v1/intelligence/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
  });

  if (!response.ok) {
    throw new Error(`Analysis request failed with status ${response.status}`);
  }

  return response.json();
}

export function getDemoResult() {
  return fallbackResult;
}

