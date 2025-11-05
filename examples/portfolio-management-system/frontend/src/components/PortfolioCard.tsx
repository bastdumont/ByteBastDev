import React from 'react';
import { Portfolio } from '../types';
import { format } from 'date-fns';

interface PortfolioCardProps {
  portfolio: Portfolio;
  onClick?: () => void;
  onDelete?: () => void;
  onRefresh?: () => void;
  isRefreshing?: boolean;
}

const PortfolioCard: React.FC<PortfolioCardProps> = ({
  portfolio,
  onClick,
  onDelete,
  onRefresh,
  isRefreshing = false,
}) => {
  // Calculate portfolio metrics
  const totalCost = portfolio.holdings.reduce(
    (sum, holding) => sum + holding.quantity * holding.purchase_price,
    0
  );

  const totalValue = portfolio.holdings.reduce(
    (sum, holding) => sum + holding.quantity * (holding.current_price || holding.purchase_price),
    0
  );

  const totalGainLoss = totalValue - totalCost;
  const totalGainLossPercent = totalCost > 0 ? (totalGainLoss / totalCost) * 100 : 0;

  const isPositive = totalGainLoss >= 0;

  return (
    <div
      className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow p-6 cursor-pointer"
      onClick={onClick}
    >
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-xl font-bold text-gray-900">{portfolio.name}</h3>
          {portfolio.description && (
            <p className="text-sm text-gray-600 mt-1">{portfolio.description}</p>
          )}
        </div>
        <div className="flex space-x-2">
          {onRefresh && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                onRefresh();
              }}
              disabled={isRefreshing}
              className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors disabled:opacity-50"
              title="Refresh prices"
            >
              <svg
                className={`w-5 h-5 ${isRefreshing ? 'animate-spin' : ''}`}
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
            </button>
          )}
          {onDelete && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                if (window.confirm(`Delete portfolio "${portfolio.name}"?`)) {
                  onDelete();
                }
              }}
              className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
              title="Delete portfolio"
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
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                />
              </svg>
            </button>
          )}
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-4">
        <div>
          <p className="text-sm text-gray-600">Total Value</p>
          <p className="text-2xl font-bold text-gray-900">
            ${totalValue.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
          </p>
        </div>
        <div>
          <p className="text-sm text-gray-600">Gain/Loss</p>
          <p
            className={`text-2xl font-bold ${
              isPositive ? 'text-green-600' : 'text-red-600'
            }`}
          >
            {isPositive ? '+' : ''}$
            {totalGainLoss.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
          </p>
        </div>
      </div>

      <div className="flex justify-between items-center pt-4 border-t border-gray-200">
        <div>
          <p className="text-sm text-gray-600">Holdings</p>
          <p className="text-lg font-semibold text-gray-900">
            {portfolio.holdings.length}
          </p>
        </div>
        <div>
          <p className="text-sm text-gray-600">Return</p>
          <p
            className={`text-lg font-semibold ${
              isPositive ? 'text-green-600' : 'text-red-600'
            }`}
          >
            {isPositive ? '+' : ''}
            {totalGainLossPercent.toFixed(2)}%
          </p>
        </div>
        <div>
          <p className="text-sm text-gray-600">Updated</p>
          <p className="text-sm text-gray-900">
            {format(new Date(portfolio.updated_at), 'MMM d, yyyy')}
          </p>
        </div>
      </div>
    </div>
  );
};

export default PortfolioCard;
