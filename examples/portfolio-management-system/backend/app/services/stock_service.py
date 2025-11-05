import yfinance as yf
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import pandas as pd
import time
from functools import lru_cache
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StockService:
    """Service for fetching stock data using yfinance with caching"""

    # Price cache: {symbol: {'price': float, 'timestamp': datetime}}
    _price_cache: Dict[str, Dict] = {}
    _cache_ttl_seconds = 60  # Cache prices for 60 seconds

    # Predefined list of popular stocks for search (avoids Yahoo Finance API rate limits)
    POPULAR_STOCKS = [
        {"symbol": "AAPL", "name": "Apple Inc.", "type": "EQUITY", "exchange": "NASDAQ"},
        {"symbol": "MSFT", "name": "Microsoft Corporation", "type": "EQUITY", "exchange": "NASDAQ"},
        {"symbol": "GOOGL", "name": "Alphabet Inc. Class A", "type": "EQUITY", "exchange": "NASDAQ"},
        {"symbol": "GOOG", "name": "Alphabet Inc. Class C", "type": "EQUITY", "exchange": "NASDAQ"},
        {"symbol": "AMZN", "name": "Amazon.com Inc.", "type": "EQUITY", "exchange": "NASDAQ"},
        {"symbol": "TSLA", "name": "Tesla Inc.", "type": "EQUITY", "exchange": "NASDAQ"},
        {"symbol": "META", "name": "Meta Platforms Inc.", "type": "EQUITY", "exchange": "NASDAQ"},
        {"symbol": "NVDA", "name": "NVIDIA Corporation", "type": "EQUITY", "exchange": "NASDAQ"},
        {"symbol": "BRK.B", "name": "Berkshire Hathaway Inc. Class B", "type": "EQUITY", "exchange": "NYSE"},
        {"symbol": "V", "name": "Visa Inc.", "type": "EQUITY", "exchange": "NYSE"},
        {"symbol": "JNJ", "name": "Johnson & Johnson", "type": "EQUITY", "exchange": "NYSE"},
        {"symbol": "WMT", "name": "Walmart Inc.", "type": "EQUITY", "exchange": "NYSE"},
        {"symbol": "JPM", "name": "JPMorgan Chase & Co.", "type": "EQUITY", "exchange": "NYSE"},
        {"symbol": "MA", "name": "Mastercard Incorporated", "type": "EQUITY", "exchange": "NYSE"},
        {"symbol": "PG", "name": "Procter & Gamble Company", "type": "EQUITY", "exchange": "NYSE"},
        {"symbol": "UNH", "name": "UnitedHealth Group Incorporated", "type": "EQUITY", "exchange": "NYSE"},
        {"symbol": "DIS", "name": "The Walt Disney Company", "type": "EQUITY", "exchange": "NYSE"},
        {"symbol": "HD", "name": "The Home Depot Inc.", "type": "EQUITY", "exchange": "NYSE"},
        {"symbol": "BAC", "name": "Bank of America Corporation", "type": "EQUITY", "exchange": "NYSE"},
        {"symbol": "ADBE", "name": "Adobe Inc.", "type": "EQUITY", "exchange": "NASDAQ"},
        {"symbol": "CRM", "name": "Salesforce Inc.", "type": "EQUITY", "exchange": "NYSE"},
        {"symbol": "NFLX", "name": "Netflix Inc.", "type": "EQUITY", "exchange": "NASDAQ"},
        {"symbol": "CMCSA", "name": "Comcast Corporation", "type": "EQUITY", "exchange": "NASDAQ"},
        {"symbol": "XOM", "name": "Exxon Mobil Corporation", "type": "EQUITY", "exchange": "NYSE"},
        {"symbol": "KO", "name": "The Coca-Cola Company", "type": "EQUITY", "exchange": "NYSE"},
        {"symbol": "PEP", "name": "PepsiCo Inc.", "type": "EQUITY", "exchange": "NASDAQ"},
        {"symbol": "COST", "name": "Costco Wholesale Corporation", "type": "EQUITY", "exchange": "NASDAQ"},
        {"symbol": "AVGO", "name": "Broadcom Inc.", "type": "EQUITY", "exchange": "NASDAQ"},
        {"symbol": "CSCO", "name": "Cisco Systems Inc.", "type": "EQUITY", "exchange": "NASDAQ"},
        {"symbol": "ORCL", "name": "Oracle Corporation", "type": "EQUITY", "exchange": "NYSE"},
        {"symbol": "INTC", "name": "Intel Corporation", "type": "EQUITY", "exchange": "NASDAQ"},
        {"symbol": "AMD", "name": "Advanced Micro Devices Inc.", "type": "EQUITY", "exchange": "NASDAQ"},
        {"symbol": "NKE", "name": "NIKE Inc.", "type": "EQUITY", "exchange": "NYSE"},
        {"symbol": "PYPL", "name": "PayPal Holdings Inc.", "type": "EQUITY", "exchange": "NASDAQ"},
        {"symbol": "T", "name": "AT&T Inc.", "type": "EQUITY", "exchange": "NYSE"},
        {"symbol": "VZ", "name": "Verizon Communications Inc.", "type": "EQUITY", "exchange": "NYSE"},
        {"symbol": "QCOM", "name": "QUALCOMM Incorporated", "type": "EQUITY", "exchange": "NASDAQ"},
        {"symbol": "TMO", "name": "Thermo Fisher Scientific Inc.", "type": "EQUITY", "exchange": "NYSE"},
        {"symbol": "MRK", "name": "Merck & Co. Inc.", "type": "EQUITY", "exchange": "NYSE"},
        {"symbol": "ABT", "name": "Abbott Laboratories", "type": "EQUITY", "exchange": "NYSE"},
        {"symbol": "CVX", "name": "Chevron Corporation", "type": "EQUITY", "exchange": "NYSE"},
        {"symbol": "PFE", "name": "Pfizer Inc.", "type": "EQUITY", "exchange": "NYSE"},
        {"symbol": "LLY", "name": "Eli Lilly and Company", "type": "EQUITY", "exchange": "NYSE"},
        {"symbol": "ABBV", "name": "AbbVie Inc.", "type": "EQUITY", "exchange": "NYSE"},
        {"symbol": "ACN", "name": "Accenture plc", "type": "EQUITY", "exchange": "NYSE"},
        {"symbol": "TXN", "name": "Texas Instruments Incorporated", "type": "EQUITY", "exchange": "NASDAQ"},
        {"symbol": "NEE", "name": "NextEra Energy Inc.", "type": "EQUITY", "exchange": "NYSE"},
        {"symbol": "DHR", "name": "Danaher Corporation", "type": "EQUITY", "exchange": "NYSE"},
        {"symbol": "UNP", "name": "Union Pacific Corporation", "type": "EQUITY", "exchange": "NYSE"},
        {"symbol": "LIN", "name": "Linde plc", "type": "EQUITY", "exchange": "NYSE"},
    ]

    @classmethod
    def _get_cached_price(cls, symbol: str) -> Optional[float]:
        """Get price from cache if not expired"""
        if symbol in cls._price_cache:
            cached = cls._price_cache[symbol]
            age = (datetime.now() - cached['timestamp']).total_seconds()
            if age < cls._cache_ttl_seconds:
                logger.debug(f"Cache hit for {symbol} (age: {age:.1f}s)")
                return cached['price']
            else:
                logger.debug(f"Cache expired for {symbol} (age: {age:.1f}s)")
        return None

    @classmethod
    def _set_cached_price(cls, symbol: str, price: float):
        """Store price in cache"""
        cls._price_cache[symbol] = {
            'price': price,
            'timestamp': datetime.now()
        }
        logger.debug(f"Cached price for {symbol}: ${price:.2f}")

    @classmethod
    def clear_cache(cls):
        """Clear all cached prices"""
        count = len(cls._price_cache)
        cls._price_cache.clear()
        logger.info(f"Cleared {count} cached prices")

    @classmethod
    def get_current_price(cls, symbol: str, max_retries: int = 3, use_cache: bool = True) -> Optional[float]:
        """
        Get current price for a stock symbol with retry logic and caching

        Uses multiple fallback methods:
        1. Cache (if enabled and not expired)
        2. Fast quote (regularMarketPrice)
        3. 1-day history close
        4. 5-day history close
        5. Previous close from info

        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL')
            max_retries: Maximum number of retry attempts
            use_cache: Whether to use cached prices

        Returns:
            Current price or None if not found
        """
        # Check cache first
        if use_cache:
            cached_price = cls._get_cached_price(symbol)
            if cached_price is not None:
                return cached_price

        for attempt in range(max_retries):
            try:
                ticker = yf.Ticker(symbol)

                # Method 1: Try fast quote first (most reliable)
                try:
                    fast_info = ticker.fast_info
                    if hasattr(fast_info, 'last_price') and fast_info.last_price:
                        price = float(fast_info.last_price)
                        logger.info(f"✓ Got price for {symbol}: ${price:.2f} (fast_info)")
                        if use_cache:
                            cls._set_cached_price(symbol, price)
                        return price
                except Exception as e:
                    logger.debug(f"Fast info failed for {symbol}: {e}")

                # Method 2: Try 1-day history
                try:
                    data = ticker.history(period="1d", interval="1d")
                    if not data.empty and 'Close' in data.columns:
                        price = float(data['Close'].iloc[-1])
                        logger.info(f"✓ Got price for {symbol}: ${price:.2f} (1d history)")
                        if use_cache:
                            cls._set_cached_price(symbol, price)
                        return price
                except Exception as e:
                    logger.debug(f"1d history failed for {symbol}: {e}")

                # Method 3: Try 5-day history as fallback
                try:
                    data = ticker.history(period="5d", interval="1d")
                    if not data.empty and 'Close' in data.columns:
                        price = float(data['Close'].iloc[-1])
                        logger.info(f"✓ Got price for {symbol}: ${price:.2f} (5d history)")
                        if use_cache:
                            cls._set_cached_price(symbol, price)
                        return price
                except Exception as e:
                    logger.debug(f"5d history failed for {symbol}: {e}")

                # Method 4: Try info dictionary
                try:
                    info = ticker.info
                    # Try multiple price fields in order of preference
                    for price_field in ['regularMarketPrice', 'currentPrice', 'previousClose']:
                        if price_field in info and info[price_field]:
                            price = float(info[price_field])
                            logger.info(f"✓ Got price for {symbol}: ${price:.2f} (info.{price_field})")
                            if use_cache:
                                cls._set_cached_price(symbol, price)
                            return price
                except Exception as e:
                    logger.debug(f"Info failed for {symbol}: {e}")

                # If we're here, all methods failed for this attempt
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2  # Exponential backoff: 2s, 4s, 6s
                    logger.warning(f"Attempt {attempt + 1} failed for {symbol}, retrying in {wait_time}s...")
                    time.sleep(wait_time)

            except Exception as e:
                logger.error(f"Error fetching price for {symbol} (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep((attempt + 1) * 2)

        logger.error(f"✗ Failed to get price for {symbol} after {max_retries} attempts")
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
        Get current prices for multiple symbols with batch optimization

        Uses yfinance's batch download capability for efficiency.

        Args:
            symbols: List of stock ticker symbols

        Returns:
            Dictionary mapping symbols to prices
        """
        quotes = {}

        if not symbols:
            return quotes

        try:
            # Method 1: Try batch download (most efficient)
            logger.info(f"Fetching prices for {len(symbols)} symbols: {', '.join(symbols)}")

            # Use yfinance download for batch fetching
            data = yf.download(
                tickers=' '.join(symbols),
                period='1d',
                interval='1d',
                group_by='ticker',
                auto_adjust=True,
                prepost=False,
                threads=True,
                progress=False
            )

            # Extract prices from batch results
            if len(symbols) == 1:
                # Single ticker case
                symbol = symbols[0]
                if not data.empty and 'Close' in data.columns:
                    quotes[symbol] = float(data['Close'].iloc[-1])
                    logger.info(f"✓ Batch got price for {symbol}: ${quotes[symbol]:.2f}")
                else:
                    quotes[symbol] = None
                    logger.warning(f"✗ No data in batch for {symbol}")
            else:
                # Multiple tickers case
                for symbol in symbols:
                    try:
                        if symbol in data.columns.get_level_values(0):
                            symbol_data = data[symbol]
                            if not symbol_data.empty and 'Close' in symbol_data.columns:
                                quotes[symbol] = float(symbol_data['Close'].iloc[-1])
                                logger.info(f"✓ Batch got price for {symbol}: ${quotes[symbol]:.2f}")
                            else:
                                quotes[symbol] = None
                                logger.warning(f"✗ No close data in batch for {symbol}")
                        else:
                            quotes[symbol] = None
                            logger.warning(f"✗ {symbol} not in batch results")
                    except Exception as e:
                        logger.error(f"Error extracting {symbol} from batch: {e}")
                        quotes[symbol] = None

        except Exception as e:
            logger.error(f"Batch download failed: {e}")
            # Fallback: fetch individually
            logger.info("Falling back to individual fetches...")
            for symbol in symbols:
                quotes[symbol] = StockService.get_current_price(symbol, max_retries=2)

        # Fill in any missing quotes with individual fetches
        missing = [sym for sym, price in quotes.items() if price is None]
        if missing:
            logger.info(f"Fetching {len(missing)} missing prices individually...")
            for symbol in missing:
                quotes[symbol] = StockService.get_current_price(symbol, max_retries=2)

        # Log summary
        successful = sum(1 for p in quotes.values() if p is not None)
        logger.info(f"Price fetch complete: {successful}/{len(symbols)} successful")

        return quotes

    @staticmethod
    def search_stocks(query: str, limit: int = 10) -> List[Dict]:
        """
        Search for stocks by name or symbol using predefined popular stocks list

        This avoids Yahoo Finance API rate limiting by searching a local list.
        Matches against both symbol and company name.

        Args:
            query: Search query (case-insensitive)
            limit: Maximum results to return

        Returns:
            List of matching stocks with symbol, name, type, and exchange
        """
        if not query:
            return []

        query_lower = query.lower().strip()
        results = []

        # Search through predefined stocks
        for stock in StockService.POPULAR_STOCKS:
            symbol_lower = stock["symbol"].lower()
            name_lower = stock["name"].lower()

            # Match if query is in symbol or name
            if (query_lower in symbol_lower or
                query_lower in name_lower or
                symbol_lower.startswith(query_lower)):
                results.append(stock.copy())

                # Stop if we've reached the limit
                if len(results) >= limit:
                    break

        return results
