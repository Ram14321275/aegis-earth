export function LoadingScreen({ message = "Initializing Systems..." }: { message?: string }) {
  return (
    <div className="flex flex-col items-center justify-center h-full w-full bg-[#0B1220]">
      <div className="w-12 h-12 border-4 border-gray-800 border-t-primary rounded-full animate-spin mb-4"></div>
      <p className="text-primary font-mono tracking-widest uppercase text-sm animate-pulse">{message}</p>
    </div>
  );
}
