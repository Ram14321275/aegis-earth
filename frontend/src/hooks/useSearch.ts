import { useState, useEffect } from "react";
import { SearchResult, SearchHistoryItem } from "../types/search";
import { SearchService } from "../services/search.service";

const HISTORY_KEY = "aegis_search_history";
const MAX_HISTORY = 10;

export function useSearch() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [history, setHistory] = useState<SearchHistoryItem[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load history on mount
  useEffect(() => {
    try {
      const stored = localStorage.getItem(HISTORY_KEY);
      if (stored) {
        setHistory(JSON.parse(stored));
      }
    } catch (e) {
      console.error("Failed to load search history", e);
    }
  }, []);

  const saveHistory = (newHistory: SearchHistoryItem[]) => {
    setHistory(newHistory);
    localStorage.setItem(HISTORY_KEY, JSON.stringify(newHistory));
  };

  const addHistoryItem = (query: string, result?: SearchResult) => {
    const item: SearchHistoryItem = {
      id: Date.now().toString(),
      query,
      timestamp: Date.now(),
      result,
    };
    
    // Remove duplicates based on query name to avoid clutter
    const filtered = history.filter(h => h.query.toLowerCase() !== query.toLowerCase());
    const updated = [item, ...filtered].slice(0, MAX_HISTORY);
    saveHistory(updated);
  };

  const performSearch = async (searchQuery: string) => {
    if (!searchQuery.trim()) {
      setResults([]);
      setError(null);
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const searchResults = await SearchService.search(searchQuery);
      setResults(searchResults);
      
      if (searchResults.length > 0) {
        // Automatically add the top result to history upon a successful submit
        addHistoryItem(searchQuery, searchResults[0]);
      } else {
        addHistoryItem(searchQuery);
      }
    } catch (err: any) {
      setError(err.message || "An error occurred during search");
      setResults([]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearHistory = () => {
    saveHistory([]);
  };

  return {
    query,
    setQuery,
    results,
    history,
    isLoading,
    error,
    performSearch,
    addHistoryItem,
    clearHistory,
    setResults // Expose to clear dropdown
  };
}
