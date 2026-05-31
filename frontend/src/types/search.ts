export type SearchResultType = "CITY" | "COUNTRY" | "COORDINATE" | "BOUNDING_BOX";

export interface SearchResult {
  id: string;
  name: string;
  type: SearchResultType;
  latitude: number;
  longitude: number;
  boundingBox?: [number, number, number, number]; // [minLat, minLng, maxLat, maxLng]
}

export interface SearchHistoryItem {
  id: string;
  query: string;
  timestamp: number;
  result?: SearchResult;
}

export interface SearchMetrics {
  search_requests_total: number;
  search_success_total: number;
  search_failures_total: number;
}
