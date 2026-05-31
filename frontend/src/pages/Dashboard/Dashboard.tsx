import { Sidebar } from "../../components/layout/Sidebar";
import { MapView } from "../../components/map/MapView";

import { SearchBar } from "../../components/search/SearchBar";

export function Dashboard() {
  return (
    <div className="flex h-full">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Panel - Search / Summary */}
        <div className="h-16 border-b border-gray-800 bg-[#0B1220] flex items-center px-6 shrink-0 justify-between">
          <div className="flex items-center gap-4 w-96 z-50">
            <SearchBar 
              onLocationSelect={(result) => {
                console.log("Location selected:", result);
                // Here we would eventually update map center or trigger backend analysis
              }}
            />
          </div>
          <div className="flex gap-4">
            <div className="bg-gray-900 border border-gray-800 px-4 py-2 rounded flex flex-col items-center">
              <span className="text-xs text-gray-500 uppercase tracking-wider">System Status</span>
              <span className="text-sm text-success font-semibold">Nominal</span>
            </div>
            <div className="bg-gray-900 border border-gray-800 px-4 py-2 rounded flex flex-col items-center">
              <span className="text-xs text-gray-500 uppercase tracking-wider">Active Alerts</span>
              <span className="text-sm text-danger font-semibold">2</span>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 flex overflow-hidden">
          {/* Map Area */}
          <div className="flex-1 bg-gray-900 relative">
            <MapView />
          </div>

          {/* Right Panel - Alerts & Risk Summary */}
          <div className="w-96 border-l border-gray-800 bg-[#0B1220] flex flex-col">
            <div className="p-4 border-b border-gray-800">
              <h2 className="text-lg font-semibold text-white tracking-wide">Risk Assessment</h2>
              <div className="mt-4 p-4 border border-danger/30 bg-danger/10 rounded-lg">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-danger font-bold">HIGH RISK</span>
                  <span className="text-gray-400 text-sm">85 / 100</span>
                </div>
                <p className="text-sm text-gray-300">Wildfire detection probability elevated in current zone. Confidence level: 92%.</p>
              </div>
            </div>
            
            <div className="flex-1 overflow-auto p-4">
              <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">Alert Stream</h3>
              <div className="space-y-3">
                {/* Placeholder Alert */}
                <div className="p-3 border border-warning/30 bg-warning/5 rounded">
                  <div className="flex justify-between">
                    <span className="text-warning text-sm font-semibold">Thermal Anomaly</span>
                    <span className="text-xs text-gray-500">2m ago</span>
                  </div>
                  <p className="text-xs text-gray-400 mt-1">Satellite metadata indicates rising surface temperatures.</p>
                </div>
                {/* Placeholder Alert */}
                <div className="p-3 border border-gray-800 rounded">
                  <div className="flex justify-between">
                    <span className="text-gray-300 text-sm font-semibold">Scan Complete</span>
                    <span className="text-xs text-gray-500">15m ago</span>
                  </div>
                  <p className="text-xs text-gray-400 mt-1">Routine area scan finished. No flood patterns detected.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
