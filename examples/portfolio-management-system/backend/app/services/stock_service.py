import yfinance as yf
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import pandas as pd

class StockService:
    """Service for fetching stock data using yfinance"""

    @staticmethod
    def get_current_price(symbol: str) -> Optional[float]:
        """
        Get current price for a stock symbol

        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL')

        Returns:
            Current price or None if not found
        """
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d")

            if data.empty:
                return None

            return float(data['Close'].iloc[-1])
        except Exception as e:
            print(f"Error fetching price for {symbol}: {e}")
            return None

    @staticmethod
    def get_stock_info(symbol: str) -> Optional[Dict]:
        """
        Get detailed information about a stock

        Args:
            symbol: Stock ticker symbol

        Returns:
            Dictionary with stock information
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info

            return {
                "symbol": symbol,
                "name": info.get("longName", ""),
                "sector": info.get("sector", ""),
                "industry": info.get("industry", ""),
                "market_cap": info.get("marketCap", 0),
                "pe_ratio": info.get("trailingPE", 0),
                "dividend_yield": info.get("dividendYield", 0),
                "52_week_high": info.get("fiftyTwoWeekHigh", 0),
                "52_week_low": info.get("fiftyTwoWeekLow", 0),
                "current_price": info.get("currentPrice", 0),
                "previous_close": info.get("previousClose", 0)
            }
        except Exception as e:
            print(f"Error fetching info for {symbol}: {e}")
            return None

    @staticmethod
    def get_historical_data(
        symbol: str,
        period: str = "1mo",
        interval: str = "1d"
    ) -> Optional[List[Dict]]:
        """
        Get historical price data

        Args:
            symbol: Stock ticker symbol
            period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            interval: Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)

        Returns:
            List of historical price points
        """
        try:
            ticker = yf.Ticker(symbol)
            history = ticker.history(period=period, interval=interval)

            if history.empty:
                return None

            # Convert to list of dictionaries
            data = []
            for index, row in history.iterrows():
                data.append({
                    "date": index.isoformat(),
                    "open": float(row['Open']),
                    "high": float(row['High']),
                    "low": float(row['Low']),
                    "close": float(row['Close']),
                    "volume": int(row['Volume'])
                })

            return data
        except Exception as e:
            print(f"Error fetching historical data for {symbol}: {e}")
            return None

    @staticmethod
    def get_multiple_quotes(symbols: List[str]) -> Dict[str, Optional[float]]:
        """
        Get current prices for multiple symbols

        Args:
            symbols: List of stock ticker symbols

        Returns:
            Dictionary mapping symbols to prices
        """
        quotes = {}
        for symbol in symbols:
            quotes[symbol] = StockService.get_current_price(symbol)
        return quotes

    @staticmethod
    def search_stocks(query: str, limit: int = 10) -> List[Dict]:
        """
        Search for stocks by name or symbol

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            List of matching stocks
        """
        try:
            # Use yfinance Ticker to validate symbol
            ticker = yf.Ticker(query.upper())
            info = ticker.info

            if info and 'symbol' in info:
                return [{
                    "symbol": info.get("symbol", query.upper()),
                    "name": info.get("longName", ""),
                    "type": info.get("quoteType", ""),
                    "exchange": info.get("exchange", "")
                }]

            return []
        except Exception as e:
            print(f"Error searching for {query}: {e}")
            return []
