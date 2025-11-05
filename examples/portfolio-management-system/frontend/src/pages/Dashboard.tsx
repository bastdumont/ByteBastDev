import React, { useState } from 'react';
import {
  usePortfolios,
  useCreatePortfolio,
  useDeletePortfolio,
} from '../hooks/usePortfolios';
import PortfolioCard from '../components/PortfolioCard';
import CreatePortfolioForm from '../components/CreatePortfolioForm';
import { CreatePortfolioRequest } from '../types';

const Dashboard: React.FC = () => {
  const [showCreateForm, setShowCreateForm] = useState(false);
  const { data: portfolios, isLoading, error } = usePortfolios();
  const createPortfolio = useCreatePortfolio();
  const deletePortfolio = useDeletePortfolio();

  const handleCreatePortfolio = async (data: CreatePortfolioRequest) => {
    try {
      await createPortfolio.mutateAsync(data);
      setShowCreateForm(false);
    } catch (err) {
      console.error('Error creating portfolio:', err);
    }
  };

  const handleDeletePortfolio = async (portfolioId: string) => {
    try {
      await deletePortfolio.mutateAsync(portfolioId);
    } catch (err) {
      console.error('Error deleting portfolio:', err);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin h-12 w-12 border-4 border-blue-500 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-gray-600">Loading portfolios...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="bg-red-50 rounded-lg p-6 max-w-md">
          <h3 className="text-red-800 font-semibold mb-2">Error Loading Portfolios</h3>
          <p className="text-red-600">{(error as any)?.message || 'Unknown error'}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Portfolio Dashboard
              </h1>
              <p className="mt-1 text-sm text-gray-600">
                Manage your investment portfolios
              </p>
            </div>
            <button
              onClick={() => setShowCreateForm(!showCreateForm)}
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
              <span>New Portfolio</span>
            </button>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Create Portfolio Form */}
        {showCreateForm && (
          <div className="mb-8">
            <CreatePortfolioForm
              onCreate={handleCreatePortfolio}
              isCreating={createPortfolio.isPending}
              onCancel={() => setShowCreateForm(false)}
            />
          </div>
        )}

        {/* Error Message */}
        {createPortfolio.isError && (
          <div className="mb-8 bg-red-50 rounded-lg p-4">
            <p className="text-red-600 text-sm">
              Error creating portfolio: {(createPortfolio.error as any)?.message || 'Unknown error'}
            </p>
          </div>
        )}

        {/* Portfolio Grid */}
        {!portfolios || portfolios.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-12 text-center">
            <svg
              className="mx-auto h-16 w-16 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"
              />
            </svg>
            <h3 className="mt-4 text-lg font-medium text-gray-900">
              No portfolios yet
            </h3>
            <p className="mt-2 text-sm text-gray-600">
              Get started by creating your first portfolio.
            </p>
            <button
              onClick={() => setShowCreateForm(true)}
              className="mt-4 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
            >
              Create Your First Portfolio
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {portfolios.map((portfolio) => (
              <PortfolioCard
                key={portfolio.id}
                portfolio={portfolio}
                onClick={() => (window.location.href = `/portfolio/${portfolio.id}`)}
                onDelete={() => handleDeletePortfolio(portfolio.id)}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
