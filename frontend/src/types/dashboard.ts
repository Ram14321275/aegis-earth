export type AlertSeverity = "INFO" | "WATCH" | "WARNING" | "CRITICAL";

export interface AlertFeedItem {
  id: string;
  severity: AlertSeverity;
  timestamp: number;
  location: string;
  summary: string;
}

export interface RiskSummaryData {
  level: "LOW" | "MODERATE" | "HIGH" | "CRITICAL";
  score: number;
  confidence: number;
  explanation: string;
}

export interface KPIMetrics {
  activeAlerts: number;
  highRiskAreas: number;
  analysesToday: number;
  systemHealth: "Nominal" | "Degraded" | "Critical";
}

export interface MapMarkerData {
  id: string;
  latitude: number;
  longitude: number;
  title: string;
  type: "wildfire" | "flood" | "sensor";
  riskScore?: number;
}
