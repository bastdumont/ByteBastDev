from typing import List, Optional, Dict
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from app.models.portfolio import Portfolio, StockHolding, PortfolioCreate, PortfolioUpdate
from app.services.stock_service import StockService

class PortfolioService:
    """Service for portfolio operations"""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.portfolios
        self.stock_service = StockService()

    async def create_portfolio(self, user_id: str, portfolio: PortfolioCreate) -> Portfolio:
        """Create a new portfolio"""
        portfolio_dict = {
            "user_id": user_id,
            "name": portfolio.name,
            "description": portfolio.description,
            "holdings": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        result = await self.collection.insert_one(portfolio_dict)
        portfolio_dict["_id"] = result.inserted_id

        return Portfolio(**portfolio_dict)

    async def get_user_portfolios(self, user_id: str) -> List[Portfolio]:
        """Get all portfolios for a user"""
        cursor = self.collection.find({"user_id": user_id})
        portfolios = await cursor.to_list(length=100)
        return [Portfolio(**p) for p in portfolios]

    async def get_portfolio(self, portfolio_id: str, user_id: str) -> Optional[Portfolio]:
        """Get a specific portfolio"""
        portfolio = await self.collection.find_one({
            "_id": ObjectId(portfolio_id),
            "user_id": user_id
        })

        if portfolio:
            return Portfolio(**portfolio)
        return None

    async def update_portfolio(
        self,
        portfolio_id: str,
        user_id: str,
        updates: PortfolioUpdate
    ) -> Optional[Portfolio]:
        """Update portfolio metadata"""
        update_dict = {k: v for k, v in updates.dict().items() if v is not None}
        update_dict["updated_at"] = datetime.utcnow()

        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(portfolio_id), "user_id": user_id},
            {"$set": update_dict},
            return_document=True
        )

        if result:
            return Portfolio(**result)
        return None

    async def delete_portfolio(self, portfolio_id: str, user_id: str) -> bool:
        """Delete a portfolio"""
        result = await self.collection.delete_one({
            "_id": ObjectId(portfolio_id),
            "user_id": user_id
        })
        return result.deleted_count > 0

    async def add_holding(
        self,
        portfolio_id: str,
        user_id: str,
        holding: StockHolding
    ) -> Optional[Portfolio]:
        """Add a stock holding to portfolio"""
        # Get current price
        current_price = self.stock_service.get_current_price(holding.symbol)
        holding.current_price = current_price

        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(portfolio_id), "user_id": user_id},
            {
                "$push": {"holdings": holding.dict()},
                "$set": {"updated_at": datetime.utcnow()}
            },
            return_document=True
        )

        if result:
            return Portfolio(**result)
        return None

    async def remove_holding(
        self,
        portfolio_id: str,
        user_id: str,
        symbol: str
    ) -> Optional[Portfolio]:
        """Remove a stock holding from portfolio"""
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(portfolio_id), "user_id": user_id},
            {
                "$pull": {"holdings": {"symbol": symbol}},
                "$set": {"updated_at": datetime.utcnow()}
            },
            return_document=True
        )

        if result:
            return Portfolio(**result)
        return None

    async def update_portfolio_prices(
        self,
        portfolio_id: str,
        user_id: str
    ) -> Optional[Portfolio]:
        """Update current prices for all holdings in portfolio"""
        portfolio = await self.get_portfolio(portfolio_id, user_id)

        if not portfolio:
            return None

        # Get all symbols
        symbols = [h.symbol for h in portfolio.holdings]

        # Fetch current prices
        quotes = self.stock_service.get_multiple_quotes(symbols)

        # Update holdings
        updated_holdings = []
        for holding in portfolio.holdings:
            holding_dict = holding.dict()
            holding_dict["current_price"] = quotes.get(holding.symbol)
            updated_holdings.append(holding_dict)

        # Update in database
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(portfolio_id), "user_id": user_id},
            {
                "$set": {
                    "holdings": updated_holdings,
                    "updated_at": datetime.utcnow()
                }
            },
            return_document=True
        )

        if result:
            return Portfolio(**result)
        return None

    def calculate_portfolio_metrics(self, portfolio: Portfolio) -> Dict:
        """Calculate portfolio performance metrics"""
        total_invested = 0
        current_value = 0

        for holding in portfolio.holdings:
            invested = holding.quantity * holding.purchase_price
            current = holding.quantity * (holding.current_price or holding.purchase_price)

            total_invested += invested
            current_value += current

        gain_loss = current_value - total_invested
        gain_loss_pct = (gain_loss / total_invested * 100) if total_invested > 0 else 0

        return {
            "total_invested": round(total_invested, 2),
            "current_value": round(current_value, 2),
            "gain_loss": round(gain_loss, 2),
            "gain_loss_percentage": round(gain_loss_pct, 2),
            "num_holdings": len(portfolio.holdings)
        }
