import { KPIMetrics, AlertFeedItem, RiskSummaryData, MapMarkerData } from "../types/dashboard";

export class DashboardService {
  static async getKPIMetrics(): Promise<KPIMetrics> {
    return new Promise(resolve => setTimeout(() => resolve({
      activeAlerts: 14,
      highRiskAreas: 3,
      analysesToday: 245,
      systemHealth: "Nominal"
    }), 500));
  }

  static async getAlertFeed(): Promise<AlertFeedItem[]> {
    return new Promise(resolve => setTimeout(() => resolve([
      {
        id: "a1",
        severity: "CRITICAL",
        timestamp: Date.now() - 1000 * 60 * 5, // 5 mins ago
        location: "California, US",
        summary: "Rapid wildfire spread detected in Napa Valley."
      },
      {
        id: "a2",
        severity: "WARNING",
        timestamp: Date.now() - 1000 * 60 * 45, // 45 mins ago
        location: "Kerala, IN",
        summary: "Precipitation models indicate high flood risk within 24h."
      },
      {
        id: "a3",
        severity: "WATCH",
        timestamp: Date.now() - 1000 * 60 * 120, // 2 hours ago
        location: "Tokyo, JP",
        summary: "Seismic sensor anomaly detected. Monitoring for secondary effects."
      },
      {
        id: "a4",
        severity: "INFO",
        timestamp: Date.now() - 1000 * 60 * 60 * 5, // 5 hours ago
        location: "Global",
        summary: "Daily sentinel analysis completed successfully."
      }
    ]), 600));
  }

  static async getRiskSummary(locationId: string = "default"): Promise<RiskSummaryData> {
    return new Promise(resolve => setTimeout(() => resolve({
      level: "HIGH",
      score: 85,
      confidence: 0.92,
      explanation: "Wildfire detection probability elevated in current zone due to rapid thermal anomalies and decreasing soil moisture."
    }), 400));
  }

  static async getMapMarkers(): Promise<MapMarkerData[]> {
    return new Promise(resolve => setTimeout(() => resolve([
      { id: "m1", latitude: 38.2975, longitude: -122.2868, title: "Napa Valley Fire", type: "wildfire", riskScore: 94 },
      { id: "m2", latitude: 10.8505, longitude: 76.2711, title: "Kerala Flood Zone", type: "flood", riskScore: 81 },
      { id: "m3", latitude: 35.6762, longitude: 139.6503, title: "Tokyo Sensor Alpha", type: "sensor", riskScore: 45 }
    ]), 500));
  }
}
