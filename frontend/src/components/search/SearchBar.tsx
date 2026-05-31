import { useState, useRef, useEffect } from "react";
import { Search, Loader2, MapPin, History, XCircle } from "lucide-react";
import { useSearch } from "../../hooks/useSearch";
import { SearchResult } from "../../types/search";

interface SearchBarProps {
  onLocationSelect?: (result: SearchResult) => void;
}

export function SearchBar({ onLocationSelect }: SearchBarProps) {
  const {
    query,
    setQuery,
    results,
    history,
    isLoading,
    error,
    performSearch,
    setResults
  } = useSearch();

  const [isOpen, setIsOpen] = useState(false);
  const wrapperRef = useRef<HTMLDivElement>(null);

  // Handle click outside to close dropdown
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // Debounce search
  useEffect(() => {
    const timer = setTimeout(() => {
      if (query.trim().length > 0) {
        performSearch(query);
      } else {
        setResults([]);
      }
    }, 300);

    return () => clearTimeout(timer);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [query]);

  const handleSelect = (result: SearchResult) => {
    setQuery(result.name);
    setIsOpen(false);
    if (onLocationSelect) {
      onLocationSelect(result);
    }
  };

  const showHistory = query.trim().length === 0 && history.length > 0;
  const showResults = query.trim().length > 0;

  return (
    <div ref={wrapperRef} className="relative w-full max-w-lg">
      <div className="relative flex items-center w-full">
        <Search className="absolute left-3 w-4 h-4 text-gray-500" />
        <input
          type="text"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setIsOpen(true);
          }}
          onFocus={() => setIsOpen(true)}
          placeholder="Search location (e.g. Tokyo, or 19.07,72.87)"
          className="w-full bg-gray-900 border border-gray-700 rounded-md pl-10 pr-4 py-2 text-sm text-white focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary placeholder:text-gray-600 transition-all"
        />
        {isLoading && (
          <Loader2 className="absolute right-3 w-4 h-4 text-primary animate-spin" />
        )}
      </div>

      {isOpen && (showHistory || showResults || error) && (
        <div className="absolute top-full left-0 w-full mt-2 bg-gray-900 border border-gray-800 rounded-md shadow-lg overflow-hidden z-50">
          
          {error && (
            <div className="p-3 text-sm text-danger flex items-center gap-2">
              <XCircle className="w-4 h-4" />
              <span>{error}</span>
            </div>
          )}

          {!error && !isLoading && showResults && results.length === 0 && (
            <div className="p-3 text-sm text-gray-500 text-center">
              No intelligence found for "{query}"
            </div>
          )}

          {!error && showResults && results.length > 0 && (
            <ul>
              {results.map((result) => (
                <li key={result.id}>
                  <button
                    onClick={() => handleSelect(result)}
                    className="w-full text-left px-4 py-2 hover:bg-gray-800 flex items-center gap-3 transition-colors"
                  >
                    <MapPin className="w-4 h-4 text-primary shrink-0" />
                    <div className="flex flex-col">
                      <span className="text-sm text-white font-medium">{result.name}</span>
                      <span className="text-xs text-gray-500">{result.type}</span>
                    </div>
                  </button>
                </li>
              ))}
            </ul>
          )}

          {showHistory && (
            <div>
              <div className="px-4 py-2 bg-gray-800/50 border-b border-gray-800 flex items-center justify-between">
                <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Recent Searches</span>
              </div>
              <ul>
                {history.map((item) => (
                  <li key={item.id}>
                    <button
                      onClick={() => {
                        if (item.result) handleSelect(item.result);
                        else setQuery(item.query);
                      }}
                      className="w-full text-left px-4 py-2 hover:bg-gray-800 flex items-center gap-3 transition-colors"
                    >
                      <History className="w-4 h-4 text-gray-500 shrink-0" />
                      <span className="text-sm text-gray-300">{item.query}</span>
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
