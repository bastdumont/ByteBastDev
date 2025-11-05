import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  usePortfolio,
  useAddHolding,
  useRemoveHolding,
  useRefreshPortfolio,
} from '../hooks/usePortfolios';
import HoldingsTable from '../components/HoldingsTable';
import AddHoldingForm from '../components/AddHoldingForm';
import PortfolioMetrics from '../components/PortfolioMetrics';
import StockChart from '../components/StockChart';
import { AddHoldingRequest } from '../types';

const PortfolioDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [selectedStock, setSelectedStock] = useState<string | null>(null);
  const [showAddForm, setShowAddForm] = useState(false);

  const { data: portfolio, isLoading, error } = usePortfolio(id);
  const addHolding = useAddHolding(id!);
  const removeHolding = useRemoveHolding(id!);
  const refreshPortfolio = useRefreshPortfolio(id!);

  const handleAddHolding = async (data: AddHoldingRequest) => {
    try {
      await addHolding.mutateAsync(data);
      setShowAddForm(false);
    } catch (err) {
      console.error('Error adding holding:', err);
    }
  };

  const handleRemoveHolding = async (symbol: string) => {
    try {
      await removeHolding.mutateAsync(symbol);
      if (selectedStock === symbol) {
        setSelectedStock(null);
      }
    } catch (err) {
      console.error('Error removing holding:', err);
    }
  };

  const handleRefresh = async () => {
    try {
      await refreshPortfolio.mutateAsync();
    } catch (err) {
      console.error('Error refreshing portfolio:', err);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin h-12 w-12 border-4 border-blue-500 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-gray-600">Loading portfolio...</p>
        </div>
      </div>
    );
  }

  if (error || !portfolio) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="bg-red-50 rounded-lg p-6 max-w-md">
          <h3 className="text-red-800 font-semibold mb-2">Error Loading Portfolio</h3>
          <p className="text-red-600">
            {(error as any)?.message || 'Portfolio not found'}
          </p>
          <button
            onClick={() => navigate('/')}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Back to Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => navigate('/')}
                className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <svg
                  className="w-6 h-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M15 19l-7-7 7-7"
                  />
                </svg>
              </button>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">
                  {portfolio.name}
                </h1>
                {portfolio.description && (
                  <p className="mt-1 text-sm text-gray-600">
                    {portfolio.description}
                  </p>
                )}
              </div>
            </div>
            <div className="flex space-x-3">
              <button
                onClick={handleRefresh}
                disabled={refreshPortfolio.isPending}
                className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors font-medium flex items-center space-x-2 disabled:opacity-50"
              >
                <svg
                  className={`w-5 h-5 ${refreshPortfolio.isPending ? 'animate-spin' : ''}`}
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                  />
                </svg>
                <span>Refresh Prices</span>
              </button>
              <button
                onClick={() => setShowAddForm(!showAddForm)}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium flex items-center space-x-2"
              >
                <svg
                  className="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 4v16m8-8H4"
                  />
                </svg>
                <span>Add Stock</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-6">
          {/* Portfolio Metrics */}
          <PortfolioMetrics portfolioId={id!} />

          {/* Add Holding Form */}
          {showAddForm && (
            <div>
              <AddHoldingForm
                portfolioId={id!}
                onAdd={handleAddHolding}
                isAdding={addHolding.isPending}
              />
              {addHolding.isError && (
                <div className="mt-4 bg-red-50 rounded-lg p-4">
                  <p className="text-red-600 text-sm">
                    Error adding holding: {(addHolding.error as any)?.message || 'Unknown error'}
                  </p>
                </div>
              )}
            </div>
          )}

          {/* Stock Chart */}
          {selectedStock && (
            <div>
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-semibold text-gray-900">
                  Stock Chart
                </h2>
                <button
                  onClick={() => setSelectedStock(null)}
                  className="text-gray-600 hover:text-gray-900"
                >
                  Close
                </button>
              </div>
              <StockChart symbol={selectedStock} period="1mo" height={400} />
            </div>
          )}

          {/* Holdings Table */}
          <div>
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              Holdings
            </h2>
            <HoldingsTable
              holdings={portfolio.holdings}
              onRemoveHolding={handleRemoveHolding}
              isRemoving={removeHolding.isPending}
            />
            {removeHolding.isError && (
              <div className="mt-4 bg-red-50 rounded-lg p-4">
                <p className="text-red-600 text-sm">
                  Error removing holding: {(removeHolding.error as any)?.message || 'Unknown error'}
                </p>
              </div>
            )}
          </div>

          {/* Stock Selection Buttons */}
          {portfolio.holdings.length > 0 && !selectedStock && (
            <div>
              <h3 className="text-sm font-medium text-gray-700 mb-2">
                View stock chart:
              </h3>
              <div className="flex flex-wrap gap-2">
                {portfolio.holdings.map((holding) => (
                  <button
                    key={holding.symbol}
                    onClick={() => setSelectedStock(holding.symbol)}
                    className="px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors text-sm font-medium"
                  >
                    {holding.symbol}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PortfolioDetail;
