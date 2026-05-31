import { AlertFeedItem } from "../../types/dashboard";
import { AlertSkeleton } from "../common/Skeleton";
import { AlertOctagon, Info, AlertTriangle, ShieldAlert } from "lucide-react";

interface AlertFeedProps {
  alerts: AlertFeedItem[];
  isLoading: boolean;
}

const severityConfig = {
  INFO: { icon: Info, colorClass: "text-primary", borderClass: "border-primary/30", bgClass: "bg-primary/5" },
  WATCH: { icon: AlertOctagon, colorClass: "text-gray-300", borderClass: "border-gray-700", bgClass: "bg-gray-800/20" },
  WARNING: { icon: AlertTriangle, colorClass: "text-warning", borderClass: "border-warning/30", bgClass: "bg-warning/5" },
  CRITICAL: { icon: ShieldAlert, colorClass: "text-danger", borderClass: "border-danger/30", bgClass: "bg-danger/10" }
};

export function AlertFeed({ alerts, isLoading }: AlertFeedProps) {
  if (isLoading) {
    return (
      <div className="space-y-3">
        <AlertSkeleton />
        <AlertSkeleton />
        <AlertSkeleton />
      </div>
    );
  }

  if (alerts.length === 0) {
    return (
      <div className="p-4 border border-gray-800 border-dashed rounded text-center">
        <span className="text-sm text-gray-500">No active alerts.</span>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {alerts.map((alert) => {
        const config = severityConfig[alert.severity];
        const Icon = config.icon;

        return (
          <div key={alert.id} className={`p-3 border rounded ${config.borderClass} ${config.bgClass}`}>
            <div className="flex justify-between items-start mb-1">
              <div className="flex items-center gap-2">
                <Icon className={`w-4 h-4 ${config.colorClass}`} />
                <span className={`text-sm font-bold ${config.colorClass}`}>{alert.severity}</span>
              </div>
              <span className="text-xs text-gray-500 whitespace-nowrap ml-2">
                {new Date(alert.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </span>
            </div>
            <div className="text-xs font-semibold text-gray-300 mb-1">{alert.location}</div>
            <p className="text-xs text-gray-400 leading-relaxed">{alert.summary}</p>
          </div>
        );
      })}
    </div>
  );
}
