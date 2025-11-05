import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';
import { useStockHistory } from '../hooks/useStocks';
import { format } from 'date-fns';

interface StockChartProps {
  symbol: string;
  period?: '1d' | '5d' | '1mo' | '3mo' | '6mo' | '1y' | '5y';
  height?: number;
}

const StockChart: React.FC<StockChartProps> = ({
  symbol,
  period = '1mo',
  height = 300,
}) => {
  const interval = period === '1d' || period === '5d' ? '1h' : '1d';
  const { data: history, isLoading, error } = useStockHistory(symbol, period, interval);

  if (isLoading) {
    return (
      <div
        className="flex items-center justify-center bg-gray-50 rounded-lg"
        style={{ height }}
      >
        <div className="text-center">
          <div className="animate-spin h-8 w-8 border-4 border-blue-500 border-t-transparent rounded-full mx-auto mb-2"></div>
          <p className="text-gray-600">Loading chart...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div
        className="flex items-center justify-center bg-red-50 rounded-lg"
        style={{ height }}
      >
        <div className="text-center text-red-600">
          <p className="font-semibold">Error loading chart</p>
          <p className="text-sm">{(error as any)?.message || 'Unknown error'}</p>
        </div>
      </div>
    );
  }

  if (!history || !history.prices || history.prices.length === 0) {
    return (
      <div
        className="flex items-center justify-center bg-gray-50 rounded-lg"
        style={{ height }}
      >
        <p className="text-gray-600">No data available</p>
      </div>
    );
  }

  // Format data for Recharts
  const chartData = history.prices.map((price) => ({
    date: format(new Date(price.date), period === '1d' ? 'HH:mm' : 'MMM dd'),
    price: price.close,
    high: price.high,
    low: price.low,
    volume: price.volume,
  }));

  // Calculate price change for color
  const firstPrice = history.prices[0]?.close || 0;
  const lastPrice = history.prices[history.prices.length - 1]?.close || 0;
  const priceChange = lastPrice - firstPrice;
  const lineColor = priceChange >= 0 ? '#10b981' : '#ef4444';

  return (
    <div className="bg-white rounded-lg p-4">
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-gray-900">{symbol}</h3>
        <p className="text-sm text-gray-600">
          {period.toUpperCase()} Price Chart
        </p>
      </div>

      <ResponsiveContainer width="100%" height={height}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis
            dataKey="date"
            tick={{ fontSize: 12 }}
            stroke="#6b7280"
          />
          <YAxis
            tick={{ fontSize: 12 }}
            stroke="#6b7280"
            domain={['auto', 'auto']}
            tickFormatter={(value) => `$${value.toFixed(2)}`}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: '#ffffff',
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
            }}
            formatter={(value: any) => [`$${value.toFixed(2)}`, 'Price']}
            labelStyle={{ color: '#374151' }}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="price"
            stroke={lineColor}
            strokeWidth={2}
            dot={false}
            name="Close Price"
            animationDuration={500}
          />
        </LineChart>
      </ResponsiveContainer>

      <div className="mt-4 flex justify-center space-x-2">
        <span className="text-sm text-gray-600">
          Range: ${Math.min(...chartData.map(d => d.low)).toFixed(2)} -
          ${Math.max(...chartData.map(d => d.high)).toFixed(2)}
        </span>
      </div>
    </div>
  );
};

export default StockChart;
