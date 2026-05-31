/**
 * Parses a coordinate string (e.g. "19.0760,72.8777", "19.0760, 72.8777")
 * Returns [latitude, longitude] if valid, otherwise null.
 */
export function parseCoordinates(input: string): [number, number] | null {
  const trimmed = input.trim();
  // Regex to match "lat,lng" or "lat, lng" with optional negatives and decimals
  const match = trimmed.match(/^([-+]?\d{1,2}(?:\.\d+)?)\s*,\s*([-+]?\d{1,3}(?:\.\d+)?)$/);
  
  if (!match) return null;

  const lat = parseFloat(match[1]);
  const lng = parseFloat(match[2]);

  // Validate bounds
  if (isNaN(lat) || isNaN(lng)) return null;
  if (lat < -90 || lat > 90) return null;
  if (lng < -180 || lng > 180) return null;

  return [lat, lng];
}
