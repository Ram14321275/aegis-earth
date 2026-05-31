import { SearchMetrics } from "../types/search";

class FrontendMetricsTracker {
  private metrics: SearchMetrics = {
    search_requests_total: 0,
    search_success_total: 0,
    search_failures_total: 0,
  };

  recordSearchRequest() {
    this.metrics.search_requests_total++;
    this.logMetrics();
  }

  recordSearchSuccess() {
    this.metrics.search_success_total++;
    this.logMetrics();
  }

  recordSearchFailure() {
    this.metrics.search_failures_total++;
    this.logMetrics();
  }

  getMetrics() {
    return { ...this.metrics };
  }

  private logMetrics() {
    // In a real app, this might batch to a backend /api/v1/telemetry endpoint
    // console.debug("[Telemetry] Frontend Metrics:", this.metrics);
  }
}

export const metricsTracker = new FrontendMetricsTracker();
