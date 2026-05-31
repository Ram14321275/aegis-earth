import { useState, useEffect } from "react";
import { Sidebar } from "../../components/layout/Sidebar";
import { MapView } from "../../components/map/MapView";
import { SearchBar } from "../../components/search/SearchBar";
import { KPICards } from "../../components/dashboard/KPICards";
import { AlertFeed } from "../../components/dashboard/AlertFeed";
import { RiskSummary } from "../../components/dashboard/RiskSummary";

import { DashboardService } from "../../services/dashboard.service";
import { KPIMetrics, AlertFeedItem, RiskSummaryData, MapMarkerData } from "../../types/dashboard";
import { SearchResult } from "../../types/search";

export function Dashboard() {
  const [metrics, setMetrics] = useState<KPIMetrics | null>(null);
  const [alerts, setAlerts] = useState<AlertFeedItem[]>([]);
  const [riskData, setRiskData] = useState<RiskSummaryData | null>(null);
  const [markers, setMarkers] = useState<MapMarkerData[]>([]);
  
  const [isLoading, setIsLoading] = useState(true);
  const [mapCenter, setMapCenter] = useState<[number, number]>([37.7749, -122.4194]);

  useEffect(() => {
    async function loadData() {
      setIsLoading(true);
      try {
        const [kpiRes, alertsRes, riskRes, markersRes] = await Promise.all([
          DashboardService.getKPIMetrics(),
          DashboardService.getAlertFeed(),
          DashboardService.getRiskSummary(),
          DashboardService.getMapMarkers()
        ]);
        
        setMetrics(kpiRes);
        setAlerts(alertsRes);
        setRiskData(riskRes);
        setMarkers(markersRes);
      } catch (err) {
        console.error("Failed to load dashboard data", err);
      } finally {
        setIsLoading(false);
      }
    }
    
    loadData();
  }, []);

  const handleLocationSelect = (result: SearchResult) => {
    setMapCenter([result.latitude, result.longitude]);
  };

  return (
    <div className="flex h-full flex-col lg:flex-row overflow-hidden">
      {/* Sidebar - hidden on mobile unless toggled (omitted toggle for brevity, hidden by default on small) */}
      <div className="hidden lg:block h-full shrink-0">
        <Sidebar />
      </div>

      <div className="flex-1 flex flex-col overflow-hidden h-full">
        {/* Top Panel - Search / Summary */}
        <div className="h-auto lg:h-16 border-b border-gray-800 bg-[#0B1220] flex flex-col lg:flex-row items-center px-4 lg:px-6 py-4 lg:py-0 shrink-0 justify-between gap-4">
          <div className="flex items-center w-full lg:w-96 z-[60]">
            <SearchBar onLocationSelect={handleLocationSelect} />
          </div>
          <div className="flex gap-4 w-full lg:w-auto overflow-x-auto pb-2 lg:pb-0 hide-scrollbar">
            <div className="bg-gray-900 border border-gray-800 px-4 py-2 rounded flex flex-col items-center shrink-0">
              <span className="text-[10px] lg:text-xs text-gray-500 uppercase tracking-wider">System Status</span>
              <span className="text-xs lg:text-sm text-success font-semibold">Nominal</span>
            </div>
            <div className="bg-gray-900 border border-gray-800 px-4 py-2 rounded flex flex-col items-center shrink-0">
              <span className="text-[10px] lg:text-xs text-gray-500 uppercase tracking-wider">Active Alerts</span>
              <span className="text-xs lg:text-sm text-danger font-semibold">2</span>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 flex flex-col lg:flex-row overflow-hidden relative">
          
          {/* Main Content Area (KPIs + Map) */}
          <div className="flex-1 flex flex-col overflow-auto bg-gray-950 p-4">
            <KPICards data={metrics} isLoading={isLoading} />
            <div className="flex-1 min-h-[400px] bg-gray-900 rounded-lg overflow-hidden border border-gray-800 z-10 relative">
              <MapView center={mapCenter} markers={markers} />
            </div>
          </div>

          {/* Right Panel - Alerts & Risk Summary */}
          <div className="w-full lg:w-96 border-t lg:border-t-0 lg:border-l border-gray-800 bg-[#0B1220] flex flex-col shrink-0 h-[50vh] lg:h-full z-20">
            <div className="p-4 border-b border-gray-800 shrink-0">
              <h2 className="text-lg font-semibold text-white tracking-wide mb-4">Risk Assessment</h2>
              <RiskSummary data={riskData} isLoading={isLoading} />
            </div>
            
            <div className="flex-1 overflow-auto p-4">
              <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4 sticky top-0 bg-[#0B1220] py-1">Alert Stream</h3>
              <AlertFeed alerts={alerts} isLoading={isLoading} />
            </div>
          </div>
          
        </div>
      </div>
    </div>
  );
}
