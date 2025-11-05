// Type definitions for Portfolio Management System

export interface StockHolding {
  symbol: string;
  quantity: number;
  purchase_price: number;
  purchase_date: string;
  current_price?: number;
}

export interface Portfolio {
  id: string;
  name: string;
  description?: string;
  user_id: string;
  holdings: StockHolding[];
  total_value?: number;
  created_at: string;
  updated_at: string;
}

export interface StockQuote {
  symbol: string;
  price: number;
  change: number;
  change_percent: number;
  volume: number;
  market_cap?: number;
  previous_close: number;
}

export interface StockInfo {
  symbol: string;
  name: string;
  sector?: string;
  industry?: string;
  description?: string;
  website?: string;
  market_cap?: number;
  pe_ratio?: number;
  dividend_yield?: number;
  fifty_two_week_high?: number;
  fifty_two_week_low?: number;
}

export interface HistoricalPrice {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface StockHistory {
  symbol: string;
  prices: HistoricalPrice[];
}

export interface PortfolioMetrics {
  total_value: number;
  total_cost: number;
  total_gain_loss: number;
  total_gain_loss_percent: number;
  holdings_count: number;
  best_performer?: {
    symbol: string;
    gain_loss_percent: number;
  };
  worst_performer?: {
    symbol: string;
    gain_loss_percent: number;
  };
}

export interface CreatePortfolioRequest {
  name: string;
  description?: string;
}

export interface AddHoldingRequest {
  symbol: string;
  quantity: number;
  purchase_price: number;
  purchase_date: string;
}

export interface SearchResult {
  symbol: string;
  name: string;
  type?: string;
  exchange?: string;
}

// API Response types
export interface ApiResponse<T> {
  data: T;
  message?: string;
}

export interface ApiError {
  detail: string;
  status?: number;
}

// UI State types
export interface LoadingState {
  isLoading: boolean;
  error: string | null;
}

export interface FormErrors {
  [key: string]: string;
}
