import { RiskSummaryData } from "../../types/dashboard";
import { Skeleton } from "../common/Skeleton";

interface RiskSummaryProps {
  data: RiskSummaryData | null;
  isLoading: boolean;
}

const levelColors = {
  LOW: "text-success border-success/30 bg-success/10",
  MODERATE: "text-warning border-warning/30 bg-warning/10",
  HIGH: "text-danger border-danger/30 bg-danger/10",
  CRITICAL: "text-danger border-danger/50 bg-danger/20 font-bold"
};

export function RiskSummary({ data, isLoading }: RiskSummaryProps) {
  if (isLoading || !data) {
    return (
      <div className="p-4 border border-gray-800 rounded-lg bg-gray-900/50 flex flex-col gap-3">
        <div className="flex justify-between">
          <Skeleton className="h-5 w-24" />
          <Skeleton className="h-5 w-16" />
        </div>
        <Skeleton className="h-16 w-full mt-2" />
      </div>
    );
  }

  const colorClass = levelColors[data.level];

  return (
    <div className={`p-4 border rounded-lg ${colorClass}`}>
      <div className="flex justify-between items-center mb-3">
        <span className="font-bold tracking-wider">{data.level} RISK</span>
        <div className="flex items-center gap-2">
          <span className="text-gray-400 text-xs">Score</span>
          <span className="font-mono">{data.score}/100</span>
        </div>
      </div>
      <p className="text-sm text-gray-300 leading-relaxed mb-3">
        {data.explanation}
      </p>
      <div className="flex items-center gap-2">
        <span className="text-xs text-gray-400 uppercase tracking-wider">Confidence</span>
        <div className="flex-1 h-1.5 bg-gray-800 rounded-full overflow-hidden">
          <div 
            className="h-full bg-current transition-all duration-1000" 
            style={{ width: `${Math.round(data.confidence * 100)}%` }} 
          />
        </div>
        <span className="text-xs font-mono">{Math.round(data.confidence * 100)}%</span>
      </div>
    </div>
  );
}
