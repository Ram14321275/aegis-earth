interface ErrorStateProps {
  title?: string;
  message?: string;
  onRetry?: () => void;
}

export function ErrorState({ title = "System Error", message = "An unexpected error occurred.", onRetry }: ErrorStateProps) {
  return (
    <div className="flex flex-col items-center justify-center h-full w-full p-6 text-center">
      <div className="w-16 h-16 rounded-full bg-danger/10 flex items-center justify-center mb-4">
        <span className="text-danger font-bold text-2xl">!</span>
      </div>
      <h3 className="text-white text-lg font-semibold mb-2">{title}</h3>
      <p className="text-gray-400 text-sm max-w-md mb-6">{message}</p>
      {onRetry && (
        <button 
          onClick={onRetry}
          className="px-4 py-2 bg-gray-800 text-white rounded hover:bg-gray-700 transition-colors"
        >
          Retry Connection
        </button>
      )}
    </div>
  );
}
