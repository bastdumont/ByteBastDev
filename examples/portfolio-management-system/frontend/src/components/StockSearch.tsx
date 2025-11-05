import React, { useState, useEffect } from 'react';
import { useStockSearch } from '../hooks/useStocks';

interface StockSearchProps {
  onSelectStock: (symbol: string) => void;
  placeholder?: string;
  className?: string;
}

const StockSearch: React.FC<StockSearchProps> = ({
  onSelectStock,
  placeholder = 'Search stocks (e.g., AAPL, TSLA)...',
  className = '',
}) => {
  const [query, setQuery] = useState('');
  const [showResults, setShowResults] = useState(false);
  const { data: results, isLoading } = useStockSearch(query);

  useEffect(() => {
    setShowResults(query.length >= 1 && !!results);
  }, [query, results]);

  const handleSelect = (symbol: string) => {
    onSelectStock(symbol);
    setQuery('');
    setShowResults(false);
  };

  const handleBlur = () => {
    // Delay to allow click on results
    setTimeout(() => setShowResults(false), 200);
  };

  return (
    <div className={`relative ${className}`}>
      <div className="relative">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onFocus={() => query.length >= 1 && setShowResults(true)}
          onBlur={handleBlur}
          placeholder={placeholder}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        {isLoading && (
          <div className="absolute right-3 top-2.5">
            <div className="animate-spin h-5 w-5 border-2 border-blue-500 border-t-transparent rounded-full"></div>
          </div>
        )}
      </div>

      {showResults && results && results.length > 0 && (
        <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg max-h-60 overflow-y-auto">
          {results.map((result: any) => (
            <button
              key={result.symbol}
              onClick={() => handleSelect(result.symbol)}
              className="w-full px-4 py-3 text-left hover:bg-gray-100 border-b border-gray-100 last:border-b-0 transition-colors"
            >
              <div className="flex justify-between items-center">
                <div>
                  <div className="font-semibold text-gray-900">
                    {result.symbol}
                  </div>
                  <div className="text-sm text-gray-600">{result.name}</div>
                </div>
                {result.exchange && (
                  <div className="text-xs text-gray-500">{result.exchange}</div>
                )}
              </div>
            </button>
          ))}
        </div>
      )}

      {showResults && results && results.length === 0 && !isLoading && (
        <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg p-4 text-center text-gray-500">
          No stocks found for "{query}"
        </div>
      )}
    </div>
  );
};

export default StockSearch;
