import { useQuery } from '@tanstack/react-query';
import { stockApi } from '../services/api';
import { StockQuote, StockInfo, StockHistory } from '../types';

// Fetch stock quote
export const useStockQuote = (symbol: string | undefined) => {
  return useQuery<StockQuote>({
    queryKey: ['stock-quote', symbol],
    queryFn: () => stockApi.getQuote(symbol!),
    enabled: !!symbol && symbol.length > 0,
    staleTime: 60000, // 1 minute
    refetchInterval: 60000, // Refetch every minute for real-time updates
  });
};

// Fetch stock info
export const useStockInfo = (symbol: string | undefined) => {
  return useQuery<StockInfo>({
    queryKey: ['stock-info', symbol],
    queryFn: () => stockApi.getInfo(symbol!),
    enabled: !!symbol && symbol.length > 0,
    staleTime: 300000, // 5 minutes (less frequent, doesn't change often)
  });
};

// Fetch stock history
export const useStockHistory = (
  symbol: string | undefined,
  period: string = '1mo',
  interval: string = '1d'
) => {
  return useQuery<StockHistory>({
    queryKey: ['stock-history', symbol, period, interval],
    queryFn: () => stockApi.getHistory(symbol!, period, interval),
    enabled: !!symbol && symbol.length > 0,
    staleTime: 300000, // 5 minutes
  });
};

// Search stocks (without auto-refetch)
export const useStockSearch = (query: string) => {
  return useQuery({
    queryKey: ['stock-search', query],
    queryFn: () => stockApi.search(query),
    enabled: query.length >= 1, // Only search if at least 1 character
    staleTime: 300000, // 5 minutes
    refetchOnWindowFocus: false, // Don't refetch on focus
  });
};
