/**
 * Exchange Rate Service
 * Fetches and caches cryptocurrency exchange rates from multiple sources
 */

import axios from 'axios';
import Redis from 'ioredis';

const redis = new Redis(process.env.REDIS_URL || 'redis://localhost:6379');

const CACHE_TTL = 60; // Cache rates for 60 seconds
const SLIPPAGE_TOLERANCE = 0.02; // 2% slippage tolerance

export interface ExchangeRate {
  cryptoCurrency: string;
  fiatCurrency: string;
  rate: number;
  source: string;
  timestamp: Date;
  validUntil: Date;
}

export interface RateQuote {
  rate: number;
  cryptoAmount: string;
  fiatAmount: number;
  spread: number;
}

/**
 * Get exchange rate from multiple sources and return average
 */
export async function getExchangeRate(
  cryptoCurrency: string,
  fiatCurrency: string = 'USD'
): Promise<ExchangeRate | null> {
  const cacheKey = `rate:${cryptoCurrency}:${fiatCurrency}`;

  try {
    // Check cache first
    const cached = await redis.get(cacheKey);
    if (cached) {
      return JSON.parse(cached);
    }

    // Fetch from multiple sources
    const rates = await Promise.allSettled([
      getCoinGeckoRate(cryptoCurrency, fiatCurrency),
      getBinanceRate(cryptoCurrency, fiatCurrency),
      getCoinMarketCapRate(cryptoCurrency, fiatCurrency)
    ]);

    // Extract successful rates
    const validRates = rates
      .filter((result): result is PromiseFulfilledResult<number> =>
        result.status === 'fulfilled' && result.value > 0
      )
      .map(result => result.value);

    if (validRates.length === 0) {
      console.error('No valid rates found');
      return null;
    }

    // Calculate average rate
    const averageRate = validRates.reduce((sum, rate) => sum + rate, 0) / validRates.length;

    // Check for outliers (rates that differ by more than slippage tolerance)
    const filteredRates = validRates.filter(rate =>
      Math.abs(rate - averageRate) / averageRate <= SLIPPAGE_TOLERANCE
    );

    // Recalculate average without outliers
    const finalRate = filteredRates.length > 0
      ? filteredRates.reduce((sum, rate) => sum + rate, 0) / filteredRates.length
      : averageRate;

    const now = new Date();
    const rateData: ExchangeRate = {
      cryptoCurrency,
      fiatCurrency,
      rate: finalRate,
      source: 'aggregated',
      timestamp: now,
      validUntil: new Date(now.getTime() + CACHE_TTL * 1000)
    };

    // Cache the rate
    await redis.setex(cacheKey, CACHE_TTL, JSON.stringify(rateData));

    // Store in database for historical tracking
    await storeRateInDatabase(rateData);

    return rateData;

  } catch (error) {
    console.error('Error fetching exchange rate:', error);
    return null;
  }
}

/**
 * Get quote for specific fiat amount
 */
export async function getQuote(
  fiatAmount: number,
  cryptoCurrency: string,
  fiatCurrency: string = 'USD'
): Promise<RateQuote | null> {
  const rateData = await getExchangeRate(cryptoCurrency, fiatCurrency);

  if (!rateData) {
    return null;
  }

  const cryptoAmount = (fiatAmount / rateData.rate).toFixed(8);
  const spread = 0.01; // 1% spread

  return {
    rate: rateData.rate,
    cryptoAmount,
    fiatAmount,
    spread
  };
}

/**
 * Fetch rate from CoinGecko
 */
async function getCoinGeckoRate(
  cryptoCurrency: string,
  fiatCurrency: string
): Promise<number> {
  try {
    const coinId = getCoinGeckoId(cryptoCurrency);
    const url = `https://api.coingecko.com/api/v3/simple/price`;

    const response = await axios.get(url, {
      params: {
        ids: coinId,
        vs_currencies: fiatCurrency.toLowerCase()
      },
      headers: {
        'x-cg-demo-api-key': process.env.COINGECKO_API_KEY
      }
    });

    return response.data[coinId][fiatCurrency.toLowerCase()];

  } catch (error) {
    console.error('CoinGecko rate fetch failed:', error);
    throw error;
  }
}

/**
 * Fetch rate from Binance
 */
async function getBinanceRate(
  cryptoCurrency: string,
  fiatCurrency: string
): Promise<number> {
  try {
    const symbol = `${cryptoCurrency}${fiatCurrency}`;
    const url = `https://api.binance.com/api/v3/ticker/price`;

    const response = await axios.get(url, {
      params: { symbol }
    });

    return parseFloat(response.data.price);

  } catch (error) {
    console.error('Binance rate fetch failed:', error);
    throw error;
  }
}

/**
 * Fetch rate from CoinMarketCap
 */
async function getCoinMarketCapRate(
  cryptoCurrency: string,
  fiatCurrency: string
): Promise<number> {
  try {
    const url = `https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest`;

    const response = await axios.get(url, {
      params: {
        symbol: cryptoCurrency,
        convert: fiatCurrency
      },
      headers: {
        'X-CMC_PRO_API_KEY': process.env.COINMARKETCAP_API_KEY
      }
    });

    const data = response.data.data[cryptoCurrency][0];
    return data.quote[fiatCurrency].price;

  } catch (error) {
    console.error('CoinMarketCap rate fetch failed:', error);
    throw error;
  }
}

/**
 * Map crypto symbols to CoinGecko IDs
 */
function getCoinGeckoId(symbol: string): string {
  const mapping: Record<string, string> = {
    'BTC': 'bitcoin',
    'ETH': 'ethereum',
    'USDC': 'usd-coin',
    'USDT': 'tether',
    'BNB': 'binancecoin',
    'SOL': 'solana',
    'ADA': 'cardano',
    'MATIC': 'matic-network'
  };

  return mapping[symbol] || symbol.toLowerCase();
}

/**
 * Store rate in database for historical tracking
 */
async function storeRateInDatabase(rateData: ExchangeRate): Promise<void> {
  try {
    // Placeholder - implement actual database storage
    console.log('Storing rate in database:', rateData);
  } catch (error) {
    console.error('Error storing rate in database:', error);
  }
}

/**
 * Get historical rates
 */
export async function getHistoricalRates(
  cryptoCurrency: string,
  fiatCurrency: string,
  days: number = 7
): Promise<ExchangeRate[]> {
  try {
    // Placeholder - implement actual database query
    return [];
  } catch (error) {
    console.error('Error fetching historical rates:', error);
    return [];
  }
}

/**
 * Calculate price impact for large orders
 */
export async function calculatePriceImpact(
  cryptoCurrency: string,
  fiatAmount: number
): Promise<number> {
  // For large orders, check liquidity and calculate slippage
  const baseAmount = 10000; // $10k base
  const impactFactor = Math.max(0, (fiatAmount - baseAmount) / 100000);

  return impactFactor * 0.01; // 1% impact per $100k above base
}
