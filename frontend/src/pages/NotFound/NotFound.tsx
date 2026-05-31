import { Link } from "react-router-dom";

export function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-7rem)] px-4">
      <h1 className="text-6xl font-bold text-danger mb-4">404</h1>
      <p className="text-xl text-gray-400 mb-8">Coordinates Not Found</p>
      <Link 
        to="/" 
        className="px-6 py-2 border border-gray-700 rounded hover:bg-gray-800 transition-colors"
      >
        Return to Base
      </Link>
    </div>
  );
}
