export function EmptyState({ message = "No data available." }: { message?: string }) {
  return (
    <div className="flex flex-col items-center justify-center h-full w-full p-6 text-center border-2 border-dashed border-gray-800 rounded-lg">
      <p className="text-gray-500 text-sm">{message}</p>
    </div>
  );
}
