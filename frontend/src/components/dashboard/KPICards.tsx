import { KPIMetrics } from "../../types/dashboard";
import { CardSkeleton } from "../common/Skeleton";
import { Activity, AlertTriangle, ShieldAlert, Cpu } from "lucide-react";

interface KPICardsProps {
  data: KPIMetrics | null;
  isLoading: boolean;
}

export function KPICards({ data, isLoading }: KPICardsProps) {
  if (isLoading || !data) {
    return (
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
        <CardSkeleton />
        <CardSkeleton />
        <CardSkeleton />
        <CardSkeleton />
      </div>
    );
  }

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
      <div className="p-4 border border-gray-800 rounded-lg bg-[#0B1220] flex flex-col hover:border-gray-700 transition-colors">
        <div className="flex justify-between items-start mb-2">
          <span className="text-gray-400 text-xs font-semibold uppercase tracking-wider">Active Alerts</span>
          <AlertTriangle className="w-4 h-4 text-warning" />
        </div>
        <span className="text-2xl font-bold text-white">{data.activeAlerts}</span>
      </div>

      <div className="p-4 border border-gray-800 rounded-lg bg-[#0B1220] flex flex-col hover:border-gray-700 transition-colors">
        <div className="flex justify-between items-start mb-2">
          <span className="text-gray-400 text-xs font-semibold uppercase tracking-wider">High Risk Areas</span>
          <ShieldAlert className="w-4 h-4 text-danger" />
        </div>
        <span className="text-2xl font-bold text-white">{data.highRiskAreas}</span>
      </div>

      <div className="p-4 border border-gray-800 rounded-lg bg-[#0B1220] flex flex-col hover:border-gray-700 transition-colors">
        <div className="flex justify-between items-start mb-2">
          <span className="text-gray-400 text-xs font-semibold uppercase tracking-wider">Analyses Today</span>
          <Activity className="w-4 h-4 text-primary" />
        </div>
        <span className="text-2xl font-bold text-white">{data.analysesToday}</span>
      </div>

      <div className="p-4 border border-gray-800 rounded-lg bg-[#0B1220] flex flex-col hover:border-gray-700 transition-colors">
        <div className="flex justify-between items-start mb-2">
          <span className="text-gray-400 text-xs font-semibold uppercase tracking-wider">System Health</span>
          <Cpu className={`w-4 h-4 ${data.systemHealth === "Nominal" ? "text-success" : "text-danger"}`} />
        </div>
        <span className={`text-xl font-bold ${data.systemHealth === "Nominal" ? "text-success" : "text-danger"}`}>
          {data.systemHealth}
        </span>
      </div>
    </div>
  );
}
