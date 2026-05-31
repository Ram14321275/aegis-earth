import { useEffect } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMap, LayersControl } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import { MapMarkerData } from "../../types/dashboard";

// Fix standard Leaflet icon paths in React
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
});

interface MapViewProps {
  center?: [number, number];
  zoom?: number;
  markers?: MapMarkerData[];
}

function MapUpdater({ center, zoom }: { center: [number, number], zoom: number }) {
  const map = useMap();
  useEffect(() => {
    map.setView(center, zoom);
  }, [center, zoom, map]);
  return null;
}

export function MapView({ center = [37.7749, -122.4194], zoom = 6, markers = [] }: MapViewProps) {
  return (
    <div className="relative w-full h-full">
      <MapContainer 
        center={center} 
        zoom={zoom} 
        scrollWheelZoom={true} 
        className="w-full h-full z-0"
      >
        <MapUpdater center={center} zoom={zoom} />
        
        <LayersControl position="topright">
          <LayersControl.BaseLayer checked name="Dark Matter (CARTO)">
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
            />
          </LayersControl.BaseLayer>
          <LayersControl.BaseLayer name="Satellite (Esri)">
            <TileLayer
              attribution="Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community"
              url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
            />
          </LayersControl.BaseLayer>

          <LayersControl.Overlay checked name="Active Hazards">
            {/* Markers represent active hazards overlay */}
            <div className="hidden">Placeholder Layer Group</div>
          </LayersControl.Overlay>
        </LayersControl>

        {markers.map((marker) => (
          <Marker key={marker.id} position={[marker.latitude, marker.longitude]}>
            <Popup className="custom-popup">
              <div className="p-1 min-w-[150px]">
                <h3 className="font-bold text-sm mb-1">{marker.title}</h3>
                <div className="flex justify-between items-center text-xs mb-1">
                  <span className="text-gray-500 uppercase tracking-wider">Type</span>
                  <span className="font-semibold">{marker.type}</span>
                </div>
                {marker.riskScore && (
                  <div className="flex justify-between items-center text-xs">
                    <span className="text-gray-500 uppercase tracking-wider">Risk Score</span>
                    <span className={`font-bold ${marker.riskScore > 80 ? 'text-danger' : marker.riskScore > 50 ? 'text-warning' : 'text-success'}`}>
                      {marker.riskScore}/100
                    </span>
                  </div>
                )}
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
      
      {/* Map UI Overlay Controls (Placeholder) */}
      <div className="absolute bottom-6 left-6 z-10 flex gap-2">
        <button className="bg-gray-900/80 backdrop-blur border border-gray-700 text-white px-3 py-1.5 rounded shadow hover:bg-gray-800 transition-colors text-xs font-semibold tracking-wider">
          HEATMAP
        </button>
        <button className="bg-gray-900/80 backdrop-blur border border-gray-700 text-white px-3 py-1.5 rounded shadow hover:bg-gray-800 transition-colors text-xs font-semibold tracking-wider">
          DIFFERENCE
        </button>
      </div>
    </div>
  );
}
