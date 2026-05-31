export type Coordinates = {
  latitude: number;
  longitude: number;
};

export type RiskBand = "low" | "moderate" | "high" | "critical";

export type DisasterSignal = {
  type: "flood" | "wildfire";
  risk: RiskBand;
  confidence: number;
  drivers: string[];
};

export type EvidenceLayer = {
  id: string;
  label: string;
  type: "map" | "heatmap" | "difference";
  description: string;
};

export type AlertItem = {
  id: string;
  severity: RiskBand;
  title: string;
  message: string;
};

export type IntelligenceResult = {
  locationName: string;
  coordinates: Coordinates;
  generatedAt: string;
  overallRisk: RiskBand;
  confidence: number;
  signals: DisasterSignal[];
  evidenceLayers: EvidenceLayer[];
  alerts: AlertItem[];
  explanation: string[];
};

export type LayerMode = "map" | "heatmap" | "difference";

