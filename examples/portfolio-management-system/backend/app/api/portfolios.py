from fastapi import APIRouter, HTTPException, Depends
from typing import List

from app.models.portfolio import (
    Portfolio,
    PortfolioCreate,
    PortfolioUpdate,
    StockHolding
)
from app.services.portfolio_service import PortfolioService
from app.api.deps import get_db, get_current_user_stub

router = APIRouter(prefix="/portfolios", tags=["portfolios"])

@router.post("", response_model=Portfolio)
async def create_portfolio(
    portfolio: PortfolioCreate,
    db=Depends(get_db),
    current_user=Depends(get_current_user_stub)
):
    """Create a new portfolio"""
    service = PortfolioService(db)
    return await service.create_portfolio(current_user, portfolio)

@router.get("", response_model=List[Portfolio])
async def get_portfolios(
    db=Depends(get_db),
    current_user=Depends(get_current_user_stub)
):
    """Get all portfolios for current user"""
    service = PortfolioService(db)
    return await service.get_user_portfolios(current_user)

@router.get("/{portfolio_id}", response_model=Portfolio)
async def get_portfolio(
    portfolio_id: str,
    db=Depends(get_db),
    current_user=Depends(get_current_user_stub)
):
    """Get a specific portfolio"""
    service = PortfolioService(db)
    portfolio = await service.get_portfolio(portfolio_id, current_user)

    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    return portfolio

@router.put("/{portfolio_id}", response_model=Portfolio)
async def update_portfolio(
    portfolio_id: str,
    updates: PortfolioUpdate,
    db=Depends(get_db),
    current_user=Depends(get_current_user_stub)
):
    """Update portfolio metadata"""
    service = PortfolioService(db)
    portfolio = await service.update_portfolio(portfolio_id, current_user, updates)

    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    return portfolio

@router.delete("/{portfolio_id}")
async def delete_portfolio(
    portfolio_id: str,
    db=Depends(get_db),
    current_user=Depends(get_current_user_stub)
):
    """Delete a portfolio"""
    service = PortfolioService(db)
    success = await service.delete_portfolio(portfolio_id, current_user)

    if not success:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    return {"message": "Portfolio deleted successfully"}

@router.post("/{portfolio_id}/holdings", response_model=Portfolio)
async def add_holding(
    portfolio_id: str,
    holding: StockHolding,
    db=Depends(get_db),
    current_user=Depends(get_current_user_stub)
):
    """Add a stock holding to portfolio"""
    service = PortfolioService(db)
    portfolio = await service.add_holding(portfolio_id, current_user, holding)

    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    return portfolio

@router.delete("/{portfolio_id}/holdings/{symbol}")
async def remove_holding(
    portfolio_id: str,
    symbol: str,
    db=Depends(get_db),
    current_user=Depends(get_current_user_stub)
):
    """Remove a stock holding from portfolio"""
    service = PortfolioService(db)
    portfolio = await service.remove_holding(portfolio_id, current_user, symbol)

    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    return portfolio

@router.post("/{portfolio_id}/refresh", response_model=Portfolio)
async def refresh_portfolio(
    portfolio_id: str,
    db=Depends(get_db),
    current_user=Depends(get_current_user_stub)
):
    """Refresh current prices for all holdings"""
    service = PortfolioService(db)
    portfolio = await service.update_portfolio_prices(portfolio_id, current_user)

    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    return portfolio

@router.get("/{portfolio_id}/metrics")
async def get_portfolio_metrics(
    portfolio_id: str,
    db=Depends(get_db),
    current_user=Depends(get_current_user_stub)
):
    """Get portfolio performance metrics"""
    service = PortfolioService(db)
    portfolio = await service.get_portfolio(portfolio_id, current_user)

    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    # Refresh prices first
    portfolio = await service.update_portfolio_prices(portfolio_id, current_user)

    metrics = service.calculate_portfolio_metrics(portfolio)
    return metrics
