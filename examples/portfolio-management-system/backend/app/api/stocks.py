from fastapi import APIRouter, HTTPException, Query
from typing import List

from app.services.stock_service import StockService

router = APIRouter(prefix="/stocks", tags=["stocks"])
stock_service = StockService()

@router.get("/quote/{symbol}")
async def get_stock_quote(symbol: str):
    """Get current quote for a stock symbol"""
    price = stock_service.get_current_price(symbol)

    if price is None:
        raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")

    return {"symbol": symbol, "price": price}

@router.get("/info/{symbol}")
async def get_stock_info(symbol: str):
    """Get detailed information about a stock"""
    info = stock_service.get_stock_info(symbol)

    if info is None:
        raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")

    return info

@router.get("/history/{symbol}")
async def get_stock_history(
    symbol: str,
    period: str = Query("1mo", regex="^(1d|5d|1mo|3mo|6mo|1y|2y|5y|10y|ytd|max)$"),
    interval: str = Query("1d", regex="^(1m|2m|5m|15m|30m|60m|90m|1h|1d|5d|1wk|1mo|3mo)$")
):
    """Get historical price data"""
    data = stock_service.get_historical_data(symbol, period, interval)

    if data is None:
        raise HTTPException(status_code=404, detail=f"No data found for {symbol}")

    return {"symbol": symbol, "period": period, "interval": interval, "data": data}

@router.get("/search")
async def search_stocks(q: str = Query(..., min_length=1), limit: int = 10):
    """Search for stocks"""
    results = stock_service.search_stocks(q, limit)
    return {"query": q, "results": results}

@router.post("/quotes")
async def get_multiple_quotes(symbols: List[str]):
    """Get quotes for multiple symbols"""
    quotes = stock_service.get_multiple_quotes(symbols)
    return {"quotes": quotes}
