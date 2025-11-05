import React from 'react';
import { usePortfolioMetrics } from '../hooks/usePortfolios';

interface PortfolioMetricsProps {
  portfolioId: string;
}

const PortfolioMetrics: React.FC<PortfolioMetricsProps> = ({ portfolioId }) => {
  const { data: metrics, isLoading, error } = usePortfolioMetrics(portfolioId);

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-4 bg-gray-200 rounded w-1/4"></div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-20 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 rounded-lg p-4">
        <p className="text-red-600 text-sm">
          Error loading metrics: {(error as any)?.message || 'Unknown error'}
        </p>
      </div>
    );
  }

  if (!metrics) {
    return null;
  }

  // Extract values from metrics (backend uses these field names)
  const totalValue = metrics.current_value ?? 0;
  const totalCost = metrics.total_invested ?? 0;
  const gainLoss = metrics.gain_loss ?? 0;
  const gainLossPercent = metrics.gain_loss_percentage ?? 0;
  const holdingsCount = metrics.num_holdings ?? 0;

  const isPositive = gainLoss >= 0;

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Portfolio Performance
      </h3>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {/* Total Value */}
        <div className="bg-blue-50 rounded-lg p-4">
          <p className="text-sm text-blue-600 font-medium mb-1">Total Value</p>
          <p className="text-2xl font-bold text-blue-900">
            ${totalValue.toLocaleString(undefined, {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2,
            })}
          </p>
        </div>

        {/* Total Cost */}
        <div className="bg-gray-50 rounded-lg p-4">
          <p className="text-sm text-gray-600 font-medium mb-1">Total Cost</p>
          <p className="text-2xl font-bold text-gray-900">
            ${totalCost.toLocaleString(undefined, {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2,
            })}
          </p>
        </div>

        {/* Gain/Loss */}
        <div
          className={`rounded-lg p-4 ${
            isPositive ? 'bg-green-50' : 'bg-red-50'
          }`}
        >
          <p
            className={`text-sm font-medium mb-1 ${
              isPositive ? 'text-green-600' : 'text-red-600'
            }`}
          >
            Gain/Loss
          </p>
          <p
            className={`text-2xl font-bold ${
              isPositive ? 'text-green-900' : 'text-red-900'
            }`}
          >
            {isPositive ? '+' : ''}$
            {gainLoss.toLocaleString(undefined, {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2,
            })}
          </p>
        </div>

        {/* Return % */}
        <div
          className={`rounded-lg p-4 ${
            isPositive ? 'bg-green-50' : 'bg-red-50'
          }`}
        >
          <p
            className={`text-sm font-medium mb-1 ${
              isPositive ? 'text-green-600' : 'text-red-600'
            }`}
          >
            Return
          </p>
          <p
            className={`text-2xl font-bold ${
              isPositive ? 'text-green-900' : 'text-red-900'
            }`}
          >
            {isPositive ? '+' : ''}
            {gainLossPercent.toFixed(2)}%
          </p>
        </div>
      </div>

      {/* Holdings Count */}
      <div className="mt-4 pt-4 border-t border-gray-200">
        <p className="text-sm text-gray-600">
          Total Holdings: <span className="font-semibold text-gray-900">{holdingsCount}</span>
        </p>
      </div>
    </div>
  );
};

export default PortfolioMetrics;
