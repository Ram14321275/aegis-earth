export type AlertSeverity = "INFO" | "WATCH" | "WARNING" | "CRITICAL" | "LOW" | "MEDIUM" | "HIGH";

export interface AlertFeedItem {
  id: string;
  severity: AlertSeverity;
  timestamp: number;
  location: string;
  summary: string;
}

export interface RiskSummaryData {
  level: "LOW" | "MODERATE" | "MEDIUM" | "HIGH" | "CRITICAL";
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
  type: "wildfire" | "flood" | "sensor" | "cyclone" | "unknown";
  riskScore?: number;
}

// Backend API schemas
export interface SystemHealthResponse {
  status: string;
  components: Record<string, any>;
}

export interface SystemMetricsResponse {
  api: { total_requests: number; successful_requests: number; failed_requests: number; average_latency_ms: number };
  cache: { cache_hits_total: number; cache_misses_total: number; cache_hit_ratio: number };
  analysis: { total_analyses: number; hazard_breakdown: Record<string, number>; average_risk_score: number };
  alerts: { alerts_generated_total: number; alerts_high_total: number; alerts_critical_total: number; alerts_generation_ms: number };
  visualizations: { requests_total: number; generation_ms: number };
  database: { queries_total: number; query_duration_ms: number; failures_total: number };
}
