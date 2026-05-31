export function Sidebar() {
  return (
    <aside className="w-64 border-r border-gray-800 bg-[#0B1220] flex flex-col h-full">
      <div className="p-4 flex flex-col gap-2">
        <button className="flex items-center gap-3 px-4 py-3 rounded bg-primary/10 text-primary hover:bg-primary/20 transition-colors text-left">
          <span>Overview</span>
        </button>
        <button className="flex items-center gap-3 px-4 py-3 rounded text-gray-400 hover:bg-gray-800 hover:text-white transition-colors text-left">
          <span>Active Alerts</span>
        </button>
        <button className="flex items-center gap-3 px-4 py-3 rounded text-gray-400 hover:bg-gray-800 hover:text-white transition-colors text-left">
          <span>Historical Analysis</span>
        </button>
      </div>
    </aside>
  );
}
