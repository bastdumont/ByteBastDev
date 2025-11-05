import React, { useState } from 'react';
import { CreatePortfolioRequest } from '../types';

interface CreatePortfolioFormProps {
  onCreate: (data: CreatePortfolioRequest) => void;
  isCreating?: boolean;
  onCancel?: () => void;
}

const CreatePortfolioForm: React.FC<CreatePortfolioFormProps> = ({
  onCreate,
  isCreating = false,
  onCancel,
}) => {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [errors, setErrors] = useState<{ [key: string]: string }>({});

  const validate = (): boolean => {
    const newErrors: { [key: string]: string } = {};

    if (!name.trim()) {
      newErrors.name = 'Portfolio name is required';
    } else if (name.length < 3) {
      newErrors.name = 'Portfolio name must be at least 3 characters';
    } else if (name.length > 100) {
      newErrors.name = 'Portfolio name must be less than 100 characters';
    }

    if (description && description.length > 500) {
      newErrors.description = 'Description must be less than 500 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!validate()) {
      return;
    }

    const data: CreatePortfolioRequest = {
      name: name.trim(),
      description: description.trim() || undefined,
    };

    onCreate(data);

    // Reset form
    setName('');
    setDescription('');
    setErrors({});
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Create New Portfolio
      </h3>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Portfolio Name */}
        <div>
          <label
            htmlFor="name"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Portfolio Name <span className="text-red-500">*</span>
          </label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="e.g., Tech Stocks, Retirement Fund"
            maxLength={100}
          />
          {errors.name && (
            <p className="mt-1 text-sm text-red-600">{errors.name}</p>
          )}
        </div>

        {/* Description */}
        <div>
          <label
            htmlFor="description"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Description (Optional)
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={3}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            placeholder="Add a description for your portfolio..."
            maxLength={500}
          />
          <p className="mt-1 text-sm text-gray-500">
            {description.length}/500 characters
          </p>
          {errors.description && (
            <p className="mt-1 text-sm text-red-600">{errors.description}</p>
          )}
        </div>

        {/* Buttons */}
        <div className="flex space-x-3">
          <button
            type="submit"
            disabled={isCreating}
            className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-medium"
          >
            {isCreating ? 'Creating...' : 'Create Portfolio'}
          </button>
          {onCancel && (
            <button
              type="button"
              onClick={onCancel}
              disabled={isCreating}
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors disabled:opacity-50 font-medium"
            >
              Cancel
            </button>
          )}
        </div>
      </form>
    </div>
  );
};

export default CreatePortfolioForm;
