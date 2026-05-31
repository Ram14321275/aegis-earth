import { SearchResult } from "../types/search";
import { parseCoordinates } from "../utils/coordinates";
import { metricsTracker } from "../lib/metrics";

// Mock Database
const MOCK_LOCATIONS: SearchResult[] = [
  { id: "1", name: "Chennai", type: "CITY", latitude: 13.0827, longitude: 80.2707 },
  { id: "2", name: "Tokyo", type: "CITY", latitude: 35.6762, longitude: 139.6503 },
  { id: "3", name: "San Francisco", type: "CITY", latitude: 37.7749, longitude: -122.4194 },
  { id: "4", name: "India", type: "COUNTRY", latitude: 20.5937, longitude: 78.9629 },
  { id: "5", name: "Japan", type: "COUNTRY", latitude: 36.2048, longitude: 138.2529 },
];

export class SearchService {
  /**
   * Simulates an API call to search for a location or coordinate.
   */
  static async search(query: string): Promise<SearchResult[]> {
    metricsTracker.recordSearchRequest();
    
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        try {
          if (!query || query.trim() === "") {
            metricsTracker.recordSearchFailure();
            return reject(new Error("Empty search query"));
          }

          // Check if it's a coordinate search
          const coords = parseCoordinates(query);
          if (coords) {
            metricsTracker.recordSearchSuccess();
            return resolve([{
              id: `coord-${Date.now()}`,
              name: `${coords[0].toFixed(4)}, ${coords[1].toFixed(4)}`,
              type: "COORDINATE",
              latitude: coords[0],
              longitude: coords[1],
            }]);
          }

          // Text Search
          const q = query.toLowerCase().trim();
          const results = MOCK_LOCATIONS.filter(loc => loc.name.toLowerCase().includes(q));
          
          metricsTracker.recordSearchSuccess();
          resolve(results);
        } catch (error) {
          metricsTracker.recordSearchFailure();
          reject(error);
        }
      }, 600); // Simulate network delay
    });
  }
}
