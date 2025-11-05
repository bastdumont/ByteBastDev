import React, { useState } from 'react';
import { AddHoldingRequest } from '../types';
import StockSearch from './StockSearch';
import { useStockQuote } from '../hooks/useStocks';

interface AddHoldingFormProps {
  portfolioId: string;
  onAdd: (data: AddHoldingRequest) => void;
  isAdding?: boolean;
}

const AddHoldingForm: React.FC<AddHoldingFormProps> = ({
  portfolioId,
  onAdd,
  isAdding = false,
}) => {
  const [selectedSymbol, setSelectedSymbol] = useState('');
  const [quantity, setQuantity] = useState('');
  const [purchasePrice, setPurchasePrice] = useState('');
  const [purchaseDate, setPurchaseDate] = useState(
    new Date().toISOString().split('T')[0]
  );
  const [errors, setErrors] = useState<{ [key: string]: string }>({});

  const { data: stockQuote } = useStockQuote(selectedSymbol);

  const handleSymbolSelect = (symbol: string) => {
    setSelectedSymbol(symbol);
    setErrors({});
  };

  const handleUsCurrentPrice = () => {
    if (stockQuote) {
      setPurchasePrice(stockQuote.price.toFixed(2));
    }
  };

  const validate = (): boolean => {
    const newErrors: { [key: string]: string } = {};

    if (!selectedSymbol) {
      newErrors.symbol = 'Please select a stock';
    }

    const qty = parseFloat(quantity);
    if (!quantity || qty <= 0) {
      newErrors.quantity = 'Quantity must be greater than 0';
    }

    const price = parseFloat(purchasePrice);
    if (!purchasePrice || price <= 0) {
      newErrors.purchasePrice = 'Purchase price must be greater than 0';
    }

    if (!purchaseDate) {
      newErrors.purchaseDate = 'Purchase date is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!validate()) {
      return;
    }

    const data: AddHoldingRequest = {
      symbol: selectedSymbol,
      quantity: parseFloat(quantity),
      purchase_price: parseFloat(purchasePrice),
      purchase_date: purchaseDate,
    };

    onAdd(data);

    // Reset form
    setSelectedSymbol('');
    setQuantity('');
    setPurchasePrice('');
    setPurchaseDate(new Date().toISOString().split('T')[0]);
    setErrors({});
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Add Stock to Portfolio
      </h3>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Stock Search */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Stock Symbol
          </label>
          <StockSearch
            onSelectStock={handleSymbolSelect}
            placeholder="Search for a stock (e.g., AAPL, TSLA)..."
          />
          {selectedSymbol && (
            <p className="mt-1 text-sm text-green-600">
              Selected: {selectedSymbol}
              {stockQuote && ` - Current Price: $${stockQuote.price.toFixed(2)}`}
            </p>
          )}
          {errors.symbol && (
            <p className="mt-1 text-sm text-red-600">{errors.symbol}</p>
          )}
        </div>

        {/* Quantity */}
        <div>
          <label
            htmlFor="quantity"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Quantity
          </label>
          <input
            type="number"
            id="quantity"
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
            step="0.001"
            min="0"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Enter number of shares"
          />
          {errors.quantity && (
            <p className="mt-1 text-sm text-red-600">{errors.quantity}</p>
          )}
        </div>

        {/* Purchase Price */}
        <div>
          <label
            htmlFor="purchasePrice"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Purchase Price
          </label>
          <div className="flex space-x-2">
            <input
              type="number"
              id="purchasePrice"
              value={purchasePrice}
              onChange={(e) => setPurchasePrice(e.target.value)}
              step="0.01"
              min="0"
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Enter purchase price"
            />
            {stockQuote && (
              <button
                type="button"
                onClick={handleUsCurrentPrice}
                className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors text-sm"
              >
                Use Current
              </button>
            )}
          </div>
          {errors.purchasePrice && (
            <p className="mt-1 text-sm text-red-600">{errors.purchasePrice}</p>
          )}
        </div>

        {/* Purchase Date */}
        <div>
          <label
            htmlFor="purchaseDate"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Purchase Date
          </label>
          <input
            type="date"
            id="purchaseDate"
            value={purchaseDate}
            onChange={(e) => setPurchaseDate(e.target.value)}
            max={new Date().toISOString().split('T')[0]}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          {errors.purchaseDate && (
            <p className="mt-1 text-sm text-red-600">{errors.purchaseDate}</p>
          )}
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isAdding}
          className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-medium"
        >
          {isAdding ? 'Adding...' : 'Add Holding'}
        </button>
      </form>
    </div>
  );
};

export default AddHoldingForm;
