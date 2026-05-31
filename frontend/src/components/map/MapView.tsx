import { MapContainer, TileLayer } from "react-leaflet";
import "leaflet/dist/leaflet.css";

// MVP MapView without backend connections
export function MapView() {
  const defaultCenter: [number, number] = [37.7749, -122.4194]; // SF

  return (
    <MapContainer 
      center={defaultCenter} 
      zoom={10} 
      scrollWheelZoom={true} 
      className="w-full h-full z-0"
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
      />
    </MapContainer>
  );
}
