# Portfolio Management System (PMS) Tutorial
## Building a Real-Time Stock Portfolio Tracker with yfinance and React

Welcome to this comprehensive tutorial on building a Portfolio Management System from scratch! This tutorial will guide you through creating a full-stack application that tracks stock portfolios, fetches real-time market data, and provides insightful analytics.

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Part 1: Backend Setup with FastAPI and yfinance](#part-1-backend-setup)
4. [Part 2: React Frontend Boilerplate](#part-2-react-frontend)
5. [Part 3: Real-Time Stock Data Integration](#part-3-real-time-data)
6. [Part 4: Portfolio Management Features](#part-4-portfolio-features)
7. [Part 5: Testing and Deployment](#part-5-testing-deployment)
8. [Bonus: Advanced Features](#bonus-advanced-features)

---

## Overview

### What We'll Build

A complete Portfolio Management System with:
- **Backend**: FastAPI + Python + yfinance for stock data
- **Frontend**: React + TypeScript + TailwindCSS
- **Database**: MongoDB for portfolio storage
- **Features**: Real-time quotes, portfolio tracking, performance analytics, charts

### Architecture

```
┌─────────────────────────────────────────────────┐
│              React Frontend                      │
│  (Portfolio Dashboard, Charts, Stock Search)     │
└──────────────────┬──────────────────────────────┘
                   │ REST API
┌──────────────────▼──────────────────────────────┐
│           FastAPI Backend                        │
│  (Authentication, Portfolio API, Stock API)      │
└──────────┬───────────────────────┬───────────────┘
           │                       │
    ┌──────▼──────┐         ┌─────▼────────┐
    │   MongoDB   │         │   yfinance   │
    │  (Storage)  │         │ (Stock Data) │
    └─────────────┘         └──────────────┘
```

---

## Prerequisites

### Required Tools

- **Python 3.9+** with pip
- **Node.js 18+** with npm
- **MongoDB** (local or MongoDB Atlas)
- **Git** for version control
- **Code editor** (VS Code recommended)

### Required Knowledge

- Basic Python programming
- Basic JavaScript/React
- Understanding of REST APIs
- Basic SQL/NoSQL concepts

### Installation

```bash
# Verify Python
python --version  # Should be 3.9+

# Verify Node.js
node --version    # Should be 18+

# Verify MongoDB
mongod --version  # Or use MongoDB Atlas
```

---

## Part 1: Backend Setup with FastAPI and yfinance {#part-1-backend-setup}

### Step 1.1: Project Structure

Create the project directory structure:

```bash
mkdir portfolio-management-system
cd portfolio-management-system

# Create backend structure
mkdir -p backend/app/{api,models,services,utils}
mkdir -p backend/tests
touch backend/app/__init__.py
touch backend/app/main.py
touch backend/requirements.txt
```

Your structure should look like:

```
portfolio-management-system/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── api/          # API routes
│   │   ├── models/       # Database models
│   │   ├── services/     # Business logic
│   │   └── utils/        # Helper functions
│   ├── tests/
│   └── requirements.txt
└── frontend/             # We'll create this in Part 2
```

### Step 1.2: Install Python Dependencies

Create `backend/requirements.txt`:

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
yfinance==0.2.32
motor==3.3.2           # Async MongoDB driver
pydantic==2.5.0
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
pandas==2.1.3
numpy==1.26.2
```

Install dependencies:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 1.3: Create Configuration

Create `backend/app/config.py`:

```python
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings"""

    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Portfolio Management System"
    VERSION: str = "1.0.0"

    # Database
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "portfolio_db"

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000"]

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

Create `backend/.env`:

```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=portfolio_db
SECRET_KEY=your-super-secret-key-here-change-in-production
```

### Step 1.4: Database Models

Create `backend/app/models/portfolio.py`:

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class StockHolding(BaseModel):
    """Individual stock holding"""
    symbol: str
    quantity: float
    purchase_price: float
    purchase_date: datetime
    current_price: Optional[float] = None

    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "AAPL",
                "quantity": 10.0,
                "purchase_price": 150.00,
                "purchase_date": "2024-01-01T00:00:00"
            }
        }

class Portfolio(BaseModel):
    """Portfolio model"""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: str
    name: str
    description: Optional[str] = None
    holdings: List[StockHolding] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "user_id": "user123",
                "name": "Tech Growth Portfolio",
                "description": "Focus on technology stocks",
                "holdings": []
            }
        }

class PortfolioCreate(BaseModel):
    """Portfolio creation model"""
    name: str
    description: Optional[str] = None

class PortfolioUpdate(BaseModel):
    """Portfolio update model"""
    name: Optional[str] = None
    description: Optional[str] = None
```

Create `backend/app/models/user.py`:

```python
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class User(BaseModel):
    """User model"""
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    disabled: Optional[bool] = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserInDB(User):
    """User in database with hashed password"""
    hashed_password: str

class UserCreate(BaseModel):
    """User registration model"""
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Token payload"""
    username: Optional[str] = None
```

### Step 1.5: Stock Data Service with yfinance

Create `backend/app/services/stock_service.py`:

```python
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
```

### Step 1.6: Portfolio Service

Create `backend/app/services/portfolio_service.py`:

```python
from typing import List, Optional
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
```

### Step 1.7: API Routes

Create `backend/app/api/stocks.py`:

```python
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

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
```

Create `backend/app/api/portfolios.py`:

```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List

from app.models.portfolio import (
    Portfolio,
    PortfolioCreate,
    PortfolioUpdate,
    StockHolding
)
from app.services.portfolio_service import PortfolioService
from app.api.deps import get_db, get_current_user

router = APIRouter(prefix="/portfolios", tags=["portfolios"])

@router.post("", response_model=Portfolio)
async def create_portfolio(
    portfolio: PortfolioCreate,
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Create a new portfolio"""
    service = PortfolioService(db)
    return await service.create_portfolio(current_user.username, portfolio)

@router.get("", response_model=List[Portfolio])
async def get_portfolios(
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Get all portfolios for current user"""
    service = PortfolioService(db)
    return await service.get_user_portfolios(current_user.username)

@router.get("/{portfolio_id}", response_model=Portfolio)
async def get_portfolio(
    portfolio_id: str,
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Get a specific portfolio"""
    service = PortfolioService(db)
    portfolio = await service.get_portfolio(portfolio_id, current_user.username)

    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    return portfolio

@router.put("/{portfolio_id}", response_model=Portfolio)
async def update_portfolio(
    portfolio_id: str,
    updates: PortfolioUpdate,
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Update portfolio metadata"""
    service = PortfolioService(db)
    portfolio = await service.update_portfolio(portfolio_id, current_user.username, updates)

    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    return portfolio

@router.delete("/{portfolio_id}")
async def delete_portfolio(
    portfolio_id: str,
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Delete a portfolio"""
    service = PortfolioService(db)
    success = await service.delete_portfolio(portfolio_id, current_user.username)

    if not success:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    return {"message": "Portfolio deleted successfully"}

@router.post("/{portfolio_id}/holdings", response_model=Portfolio)
async def add_holding(
    portfolio_id: str,
    holding: StockHolding,
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Add a stock holding to portfolio"""
    service = PortfolioService(db)
    portfolio = await service.add_holding(portfolio_id, current_user.username, holding)

    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    return portfolio

@router.delete("/{portfolio_id}/holdings/{symbol}")
async def remove_holding(
    portfolio_id: str,
    symbol: str,
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Remove a stock holding from portfolio"""
    service = PortfolioService(db)
    portfolio = await service.remove_holding(portfolio_id, current_user.username, symbol)

    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    return portfolio

@router.post("/{portfolio_id}/refresh", response_model=Portfolio)
async def refresh_portfolio(
    portfolio_id: str,
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Refresh current prices for all holdings"""
    service = PortfolioService(db)
    portfolio = await service.update_portfolio_prices(portfolio_id, current_user.username)

    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    return portfolio

@router.get("/{portfolio_id}/metrics")
async def get_portfolio_metrics(
    portfolio_id: str,
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Get portfolio performance metrics"""
    service = PortfolioService(db)
    portfolio = await service.get_portfolio(portfolio_id, current_user.username)

    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    # Refresh prices first
    portfolio = await service.update_portfolio_prices(portfolio_id, current_user.username)

    metrics = service.calculate_portfolio_metrics(portfolio)
    return metrics
```

### Step 1.8: Dependencies and Database Connection

Create `backend/app/api/deps.py`:

```python
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.config import settings
from app.models.user import User, TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/auth/login")

# Database client (singleton)
_db_client: AsyncIOMotorClient = None

async def get_db() -> AsyncIOMotorDatabase:
    """Get database instance"""
    global _db_client

    if _db_client is None:
        _db_client = AsyncIOMotorClient(settings.MONGODB_URL)

    return _db_client[settings.DATABASE_NAME]

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    # For simplicity, return a user object
    # In production, query from database
    return User(username=token_data.username, email=f"{token_data.username}@example.com")
```

### Step 1.9: Main Application

Create `backend/app/main.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api import stocks, portfolios

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(stocks.router, prefix=settings.API_V1_PREFIX)
app.include_router(portfolios.router, prefix=settings.API_V1_PREFIX)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Portfolio Management System API",
        "version": settings.VERSION,
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
```

### Step 1.10: Run the Backend

```bash
# Make sure you're in the backend directory with venv activated
cd backend
source venv/bin/activate

# Run the development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Visit http://localhost:8000/docs to see the interactive API documentation!

---

## Part 2: React Frontend Boilerplate {#part-2-react-frontend}

### Step 2.1: Create React App

```bash
# Go back to project root
cd ..

# Create React app with TypeScript
npx create-react-app frontend --template typescript

cd frontend
```

### Step 2.2: Install Dependencies

```bash
npm install axios react-router-dom @tanstack/react-query
npm install recharts date-fns
npm install -D tailwindcss postcss autoprefixer
npm install @headlessui/react @heroicons/react

# Initialize Tailwind
npx tailwindcss init -p
```

### Step 2.3: Configure Tailwind CSS

Update `frontend/tailwind.config.js`:

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

Update `frontend/src/index.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### Step 2.4: Project Structure

Create the following structure:

```
frontend/src/
├── components/
│   ├── layout/
│   ├── portfolio/
│   ├── stocks/
│   └── common/
├── pages/
│   ├── Dashboard.tsx
│   ├── Portfolio.tsx
│   └── StockSearch.tsx
├── services/
│   └── api.ts
├── hooks/
│   ├── useStocks.ts
│   └── usePortfolio.ts
├── types/
│   └── index.ts
├── utils/
│   └── helpers.ts
├── App.tsx
└── index.tsx
```

### Step 2.5: Type Definitions

Create `frontend/src/types/index.ts`:

```typescript
export interface StockHolding {
  symbol: string;
  quantity: number;
  purchase_price: number;
  purchase_date: string;
  current_price?: number;
}

export interface Portfolio {
  _id?: string;
  user_id: string;
  name: string;
  description?: string;
  holdings: StockHolding[];
  created_at: string;
  updated_at: string;
}

export interface StockQuote {
  symbol: string;
  price: number;
}

export interface StockInfo {
  symbol: string;
  name: string;
  sector: string;
  industry: string;
  market_cap: number;
  pe_ratio: number;
  dividend_yield: number;
  '52_week_high': number;
  '52_week_low': number;
  current_price: number;
  previous_close: number;
}

export interface HistoricalDataPoint {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface PortfolioMetrics {
  total_invested: number;
  current_value: number;
  gain_loss: number;
  gain_loss_percentage: number;
  num_holdings: number;
}
```

### Step 2.6: API Service

Create `frontend/src/services/api.ts`:

```typescript
import axios from 'axios';
import {
  Portfolio,
  StockQuote,
  StockInfo,
  HistoricalDataPoint,
  StockHolding,
  PortfolioMetrics
} from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Stock API
export const stockApi = {
  getQuote: async (symbol: string): Promise<StockQuote> => {
    const response = await api.get(`/stocks/quote/${symbol}`);
    return response.data;
  },

  getInfo: async (symbol: string): Promise<StockInfo> => {
    const response = await api.get(`/stocks/info/${symbol}`);
    return response.data;
  },

  getHistory: async (
    symbol: string,
    period: string = '1mo',
    interval: string = '1d'
  ): Promise<HistoricalDataPoint[]> => {
    const response = await api.get(`/stocks/history/${symbol}`, {
      params: { period, interval }
    });
    return response.data.data;
  },

  search: async (query: string): Promise<any[]> => {
    const response = await api.get('/stocks/search', {
      params: { q: query }
    });
    return response.data.results;
  },
};

// Portfolio API
export const portfolioApi = {
  getAll: async (): Promise<Portfolio[]> => {
    const response = await api.get('/portfolios');
    return response.data;
  },

  getById: async (id: string): Promise<Portfolio> => {
    const response = await api.get(`/portfolios/${id}`);
    return response.data;
  },

  create: async (data: { name: string; description?: string }): Promise<Portfolio> => {
    const response = await api.post('/portfolios', data);
    return response.data;
  },

  update: async (id: string, data: Partial<Portfolio>): Promise<Portfolio> => {
    const response = await api.put(`/portfolios/${id}`, data);
    return response.data;
  },

  delete: async (id: string): Promise<void> => {
    await api.delete(`/portfolios/${id}`);
  },

  addHolding: async (id: string, holding: StockHolding): Promise<Portfolio> => {
    const response = await api.post(`/portfolios/${id}/holdings`, holding);
    return response.data;
  },

  removeHolding: async (id: string, symbol: string): Promise<Portfolio> => {
    const response = await api.delete(`/portfolios/${id}/holdings/${symbol}`);
    return response.data;
  },

  refresh: async (id: string): Promise<Portfolio> => {
    const response = await api.post(`/portfolios/${id}/refresh`);
    return response.data;
  },

  getMetrics: async (id: string): Promise<PortfolioMetrics> => {
    const response = await api.get(`/portfolios/${id}/metrics`);
    return response.data;
  },
};

export default api;
```

### Step 2.7: Custom Hooks

Create `frontend/src/hooks/useStocks.ts`:

```typescript
import { useQuery } from '@tanstack/react-query';
import { stockApi } from '../services/api';

export const useStockQuote = (symbol: string) => {
  return useQuery({
    queryKey: ['stock-quote', symbol],
    queryFn: () => stockApi.getQuote(symbol),
    enabled: !!symbol,
    refetchInterval: 60000, // Refresh every minute
  });
};

export const useStockInfo = (symbol: string) => {
  return useQuery({
    queryKey: ['stock-info', symbol],
    queryFn: () => stockApi.getInfo(symbol),
    enabled: !!symbol,
  });
};

export const useStockHistory = (
  symbol: string,
  period: string = '1mo',
  interval: string = '1d'
) => {
  return useQuery({
    queryKey: ['stock-history', symbol, period, interval],
    queryFn: () => stockApi.getHistory(symbol, period, interval),
    enabled: !!symbol,
  });
};
```

Create `frontend/src/hooks/usePortfolio.ts`:

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { portfolioApi } from '../services/api';
import { Portfolio, StockHolding } from '../types';

export const usePortfolios = () => {
  return useQuery({
    queryKey: ['portfolios'],
    queryFn: portfolioApi.getAll,
  });
};

export const usePortfolio = (id: string) => {
  return useQuery({
    queryKey: ['portfolio', id],
    queryFn: () => portfolioApi.getById(id),
    enabled: !!id,
  });
};

export const usePortfolioMetrics = (id: string) => {
  return useQuery({
    queryKey: ['portfolio-metrics', id],
    queryFn: () => portfolioApi.getMetrics(id),
    enabled: !!id,
  });
};

export const useCreatePortfolio = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: portfolioApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['portfolios'] });
    },
  });
};

export const useAddHolding = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ portfolioId, holding }: { portfolioId: string; holding: StockHolding }) =>
      portfolioApi.addHolding(portfolioId, holding),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['portfolio', variables.portfolioId] });
      queryClient.invalidateQueries({ queryKey: ['portfolio-metrics', variables.portfolioId] });
    },
  });
};

export const useRemoveHolding = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ portfolioId, symbol }: { portfolioId: string; symbol: string }) =>
      portfolioApi.removeHolding(portfolioId, symbol),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['portfolio', variables.portfolioId] });
      queryClient.invalidateQueries({ queryKey: ['portfolio-metrics', variables.portfolioId] });
    },
  });
};

export const useRefreshPortfolio = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: portfolioApi.refresh,
    onSuccess: (_, portfolioId) => {
      queryClient.invalidateQueries({ queryKey: ['portfolio', portfolioId] });
      queryClient.invalidateQueries({ queryKey: ['portfolio-metrics', portfolioId] });
    },
  });
};
```

### Step 2.8: Continue to Part 3

The frontend boilerplate is now set up! In Part 3, we'll build the actual UI components.

---

## Part 3: Real-Time Stock Data Integration {#part-3-real-time-data}

### Step 3.1: Stock Chart Component

Create `frontend/src/components/stocks/StockChart.tsx`:

```typescript
import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts';
import { format, parseISO } from 'date-fns';
import { HistoricalDataPoint } from '../../types';

interface StockChartProps {
  data: HistoricalDataPoint[];
  symbol: string;
}

export const StockChart: React.FC<StockChartProps> = ({ data, symbol }) => {
  const formattedData = data.map(point => ({
    ...point,
    date: format(parseISO(point.date), 'MMM dd'),
  }));

  return (
    <div className="w-full h-96 bg-white p-4 rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-4">{symbol} Price History</h3>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={formattedData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis domain={['auto', 'auto']} />
          <Tooltip
            formatter={(value: number) => `$${value.toFixed(2)}`}
            labelFormatter={(label) => `Date: ${label}`}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="close"
            stroke="#2563eb"
            strokeWidth={2}
            dot={false}
            name="Close Price"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};
```

### Step 3.2: Stock Search Component

Create `frontend/src/components/stocks/StockSearch.tsx`:

```typescript
import React, { useState } from 'react';
import { MagnifyingGlassIcon } from '@heroicons/react/24/outline';
import { stockApi } from '../../services/api';

interface StockSearchProps {
  onSelect: (symbol: string) => void;
}

export const StockSearch: React.FC<StockSearchProps> = ({ onSelect }) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (searchQuery: string) => {
    setQuery(searchQuery);

    if (searchQuery.length < 1) {
      setResults([]);
      return;
    }

    setLoading(true);
    try {
      const searchResults = await stockApi.search(searchQuery);
      setResults(searchResults);
    } catch (error) {
      console.error('Search error:', error);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSelect = (symbol: string) => {
    onSelect(symbol);
    setQuery('');
    setResults([]);
  };

  return (
    <div className="relative">
      <div className="relative">
        <MagnifyingGlassIcon className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
        <input
          type="text"
          value={query}
          onChange={(e) => handleSearch(e.target.value)}
          placeholder="Search stocks by symbol (e.g., AAPL)"
          className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      {loading && (
        <div className="absolute z-10 w-full mt-2 bg-white rounded-lg shadow-lg p-4">
          <p className="text-gray-500">Searching...</p>
        </div>
      )}

      {results.length > 0 && !loading && (
        <div className="absolute z-10 w-full mt-2 bg-white rounded-lg shadow-lg max-h-60 overflow-y-auto">
          {results.map((result) => (
            <button
              key={result.symbol}
              onClick={() => handleSelect(result.symbol)}
              className="w-full px-4 py-3 text-left hover:bg-gray-100 border-b last:border-b-0"
            >
              <div className="font-semibold">{result.symbol}</div>
              <div className="text-sm text-gray-600">{result.name}</div>
              <div className="text-xs text-gray-400">{result.exchange}</div>
            </button>
          ))}
        </div>
      )}
    </div>
  );
};
```

### Step 3.3: Stock Info Card

Create `frontend/src/components/stocks/StockInfoCard.tsx`:

```typescript
import React from 'react';
import { StockInfo } from '../../types';
import { ArrowTrendingUpIcon, ArrowTrendingDownIcon } from '@heroicons/react/24/outline';

interface StockInfoCardProps {
  info: StockInfo;
}

export const StockInfoCard: React.FC<StockInfoCardProps> = ({ info }) => {
  const priceChange = info.current_price - info.previous_close;
  const priceChangePercent = (priceChange / info.previous_close) * 100;
  const isPositive = priceChange >= 0;

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h2 className="text-2xl font-bold">{info.symbol}</h2>
          <p className="text-gray-600">{info.name}</p>
        </div>
        <div className="text-right">
          <div className="text-3xl font-bold">${info.current_price.toFixed(2)}</div>
          <div className={`flex items-center ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
            {isPositive ? (
              <ArrowTrendingUpIcon className="h-4 w-4 mr-1" />
            ) : (
              <ArrowTrendingDownIcon className="h-4 w-4 mr-1" />
            )}
            <span>
              {priceChange.toFixed(2)} ({priceChangePercent.toFixed(2)}%)
            </span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 text-sm">
        <div>
          <p className="text-gray-500">Sector</p>
          <p className="font-semibold">{info.sector || 'N/A'}</p>
        </div>
        <div>
          <p className="text-gray-500">Industry</p>
          <p className="font-semibold">{info.industry || 'N/A'}</p>
        </div>
        <div>
          <p className="text-gray-500">Market Cap</p>
          <p className="font-semibold">
            ${(info.market_cap / 1e9).toFixed(2)}B
          </p>
        </div>
        <div>
          <p className="text-gray-500">P/E Ratio</p>
          <p className="font-semibold">{info.pe_ratio.toFixed(2)}</p>
        </div>
        <div>
          <p className="text-gray-500">52 Week High</p>
          <p className="font-semibold">${info['52_week_high'].toFixed(2)}</p>
        </div>
        <div>
          <p className="text-gray-500">52 Week Low</p>
          <p className="font-semibold">${info['52_week_low'].toFixed(2)}</p>
        </div>
      </div>
    </div>
  );
};
```

---

## Part 4: Portfolio Management Features {#part-4-portfolio-features}

### Step 4.1: Portfolio Card Component

Create `frontend/src/components/portfolio/PortfolioCard.tsx`:

```typescript
import React from 'react';
import { Link } from 'react-router-dom';
import { Portfolio } from '../../types';
import { ChartBarIcon, PlusIcon } from '@heroicons/react/24/outline';

interface PortfolioCardProps {
  portfolio: Portfolio;
}

export const PortfolioCard: React.FC<PortfolioCardProps> = ({ portfolio }) => {
  const holdingsCount = portfolio.holdings.length;

  return (
    <Link
      to={`/portfolio/${portfolio._id}`}
      className="block bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
    >
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-xl font-semibold">{portfolio.name}</h3>
          <p className="text-gray-600 text-sm mt-1">{portfolio.description}</p>
        </div>
        <ChartBarIcon className="h-8 w-8 text-blue-500" />
      </div>

      <div className="flex items-center justify-between text-sm">
        <span className="text-gray-500">{holdingsCount} holdings</span>
        <span className="text-gray-400">
          Updated {new Date(portfolio.updated_at).toLocaleDateString()}
        </span>
      </div>
    </Link>
  );
};
```

### Step 4.2: Add Holding Form

Create `frontend/src/components/portfolio/AddHoldingForm.tsx`:

```typescript
import React, { useState } from 'react';
import { StockSearch } from '../stocks/StockSearch';
import { StockHolding } from '../../types';

interface AddHoldingFormProps {
  onAdd: (holding: StockHolding) => void;
  onCancel: () => void;
}

export const AddHoldingForm: React.FC<AddHoldingFormProps> = ({ onAdd, onCancel }) => {
  const [selectedSymbol, setSelectedSymbol] = useState('');
  const [quantity, setQuantity] = useState('');
  const [purchasePrice, setpurchasePrice] = useState('');
  const [purchaseDate, setPurchaseDate] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!selectedSymbol || !quantity || !purchasePrice || !purchaseDate) {
      alert('Please fill in all fields');
      return;
    }

    const holding: StockHolding = {
      symbol: selectedSymbol,
      quantity: parseFloat(quantity),
      purchase_price: parseFloat(purchasePrice),
      purchase_date: new Date(purchaseDate).toISOString(),
    };

    onAdd(holding);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg p-6 max-w-md w-full">
        <h2 className="text-2xl font-bold mb-4">Add Stock Holding</h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Stock Symbol
            </label>
            <StockSearch onSelect={setSelectedSymbol} />
            {selectedSymbol && (
              <p className="mt-2 text-sm text-green-600">Selected: {selectedSymbol}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Quantity
            </label>
            <input
              type="number"
              step="0.01"
              value={quantity}
              onChange={(e) => setQuantity(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="e.g., 10"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Purchase Price ($)
            </label>
            <input
              type="number"
              step="0.01"
              value={purchasePrice}
              onChange={(e) => setpurchasePrice(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="e.g., 150.00"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Purchase Date
            </label>
            <input
              type="date"
              value={purchaseDate}
              onChange={(e) => setPurchaseDate(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div className="flex space-x-3 pt-4">
            <button
              type="submit"
              className="flex-1 bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Add Holding
            </button>
            <button
              type="button"
              onClick={onCancel}
              className="flex-1 bg-gray-200 text-gray-700 py-2 rounded-lg hover:bg-gray-300 transition-colors"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
```

### Step 4.3: Holdings Table

Create `frontend/src/components/portfolio/HoldingsTable.tsx`:

```typescript
import React from 'react';
import { StockHolding } from '../../types';
import { TrashIcon } from '@heroicons/react/24/outline';

interface HoldingsTableProps {
  holdings: StockHolding[];
  onRemove: (symbol: string) => void;
}

export const HoldingsTable: React.FC<HoldingsTableProps> = ({ holdings, onRemove }) => {
  const calculateGainLoss = (holding: StockHolding) => {
    if (!holding.current_price) return { amount: 0, percentage: 0 };

    const invested = holding.quantity * holding.purchase_price;
    const current = holding.quantity * holding.current_price;
    const amount = current - invested;
    const percentage = (amount / invested) * 100;

    return { amount, percentage };
  };

  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Symbol
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Quantity
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Purchase Price
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Current Price
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Gain/Loss
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Actions
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {holdings.map((holding) => {
            const { amount, percentage } = calculateGainLoss(holding);
            const isPositive = amount >= 0;

            return (
              <tr key={holding.symbol} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap font-semibold">
                  {holding.symbol}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  {holding.quantity}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  ${holding.purchase_price.toFixed(2)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  {holding.current_price ? `$${holding.current_price.toFixed(2)}` : 'Loading...'}
                </td>
                <td className={`px-6 py-4 whitespace-nowrap ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
                  {holding.current_price ? (
                    <>
                      ${amount.toFixed(2)} ({percentage.toFixed(2)}%)
                    </>
                  ) : (
                    '-'
                  )}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <button
                    onClick={() => onRemove(holding.symbol)}
                    className="text-red-600 hover:text-red-900"
                  >
                    <TrashIcon className="h-5 w-5" />
                  </button>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};
```

### Step 4.4: Portfolio Metrics Dashboard

Create `frontend/src/components/portfolio/PortfolioMetrics.tsx`:

```typescript
import React from 'react';
import { PortfolioMetrics } from '../../types';
import {
  BanknotesIcon,
  ChartBarIcon,
  ArrowTrendingUpIcon,
  CubeIcon
} from '@heroicons/react/24/outline';

interface PortfolioMetricsProps {
  metrics: PortfolioMetrics;
}

export const PortfolioMetricsDisplay: React.FC<PortfolioMetricsProps> = ({ metrics }) => {
  const isPositive = metrics.gain_loss >= 0;

  const cards = [
    {
      title: 'Total Invested',
      value: `$${metrics.total_invested.toLocaleString()}`,
      icon: BanknotesIcon,
      color: 'blue',
    },
    {
      title: 'Current Value',
      value: `$${metrics.current_value.toLocaleString()}`,
      icon: ChartBarIcon,
      color: 'green',
    },
    {
      title: 'Gain/Loss',
      value: `$${metrics.gain_loss.toLocaleString()}`,
      subValue: `${metrics.gain_loss_percentage.toFixed(2)}%`,
      icon: ArrowTrendingUpIcon,
      color: isPositive ? 'green' : 'red',
    },
    {
      title: 'Holdings',
      value: metrics.num_holdings.toString(),
      icon: CubeIcon,
      color: 'purple',
    },
  ];

  const colorClasses = {
    blue: 'bg-blue-100 text-blue-600',
    green: 'bg-green-100 text-green-600',
    red: 'bg-red-100 text-red-600',
    purple: 'bg-purple-100 text-purple-600',
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {cards.map((card) => {
        const Icon = card.icon;
        return (
          <div key={card.title} className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between mb-2">
              <p className="text-sm text-gray-600">{card.title}</p>
              <div className={`p-2 rounded-lg ${colorClasses[card.color as keyof typeof colorClasses]}`}>
                <Icon className="h-6 w-6" />
              </div>
            </div>
            <p className="text-2xl font-bold">{card.value}</p>
            {card.subValue && (
              <p className={`text-sm mt-1 ${card.color === 'red' ? 'text-red-600' : 'text-green-600'}`}>
                {card.subValue}
              </p>
            )}
          </div>
        );
      })}
    </div>
  );
};
```

### Step 4.5: Main App Component

Update `frontend/src/App.tsx`:

```typescript
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Dashboard } from './pages/Dashboard';
import { PortfolioDetail } from './pages/PortfolioDetail';
import { StockSearchPage } from './pages/StockSearchPage';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="min-h-screen bg-gray-100">
          <nav className="bg-white shadow-sm">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="flex justify-between h-16 items-center">
                <div className="flex space-x-8">
                  <Link to="/" className="text-xl font-bold text-gray-900">
                    Portfolio Manager
                  </Link>
                  <Link to="/" className="text-gray-600 hover:text-gray-900">
                    Dashboard
                  </Link>
                  <Link to="/search" className="text-gray-600 hover:text-gray-900">
                    Search Stocks
                  </Link>
                </div>
              </div>
            </div>
          </nav>

          <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/portfolio/:id" element={<PortfolioDetail />} />
              <Route path="/search" element={<StockSearchPage />} />
            </Routes>
          </main>
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
```

---

## Part 5: Testing and Deployment {#part-5-testing-deployment}

### Step 5.1: Backend Tests

Create `backend/tests/test_stock_service.py`:

```python
import pytest
from app.services.stock_service import StockService

def test_get_current_price():
    """Test fetching current stock price"""
    service = StockService()
    price = service.get_current_price("AAPL")

    assert price is not None
    assert isinstance(price, float)
    assert price > 0

def test_get_stock_info():
    """Test fetching stock information"""
    service = StockService()
    info = service.get_stock_info("AAPL")

    assert info is not None
    assert info["symbol"] == "AAPL"
    assert "name" in info
    assert "sector" in info

def test_get_historical_data():
    """Test fetching historical data"""
    service = StockService()
    data = service.get_historical_data("AAPL", period="5d", interval="1d")

    assert data is not None
    assert len(data) > 0
    assert "date" in data[0]
    assert "close" in data[0]
```

Run tests:

```bash
cd backend
pytest tests/
```

### Step 5.2: Frontend Tests

Create `frontend/src/components/__tests__/PortfolioCard.test.tsx`:

```typescript
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { PortfolioCard } from '../portfolio/PortfolioCard';
import { Portfolio } from '../../types';

const mockPortfolio: Portfolio = {
  _id: '1',
  user_id: 'user1',
  name: 'Test Portfolio',
  description: 'A test portfolio',
  holdings: [],
  created_at: '2024-01-01T00:00:00Z',
  updated_at: '2024-01-01T00:00:00Z',
};

test('renders portfolio card', () => {
  render(
    <BrowserRouter>
      <PortfolioCard portfolio={mockPortfolio} />
    </BrowserRouter>
  );

  expect(screen.getByText('Test Portfolio')).toBeInTheDocument();
  expect(screen.getByText('A test portfolio')).toBeInTheDocument();
});
```

### Step 5.3: Docker Setup

Create `docker-compose.yml` in project root:

```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:7.0
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    environment:
      MONGO_INITDB_DATABASE: portfolio_db

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      MONGODB_URL: mongodb://mongodb:27017
      DATABASE_NAME: portfolio_db
    depends_on:
      - mongodb
    volumes:
      - ./backend:/app

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      REACT_APP_API_URL: http://localhost:8000/api/v1
    volumes:
      - ./frontend:/app
      - /app/node_modules

volumes:
  mongodb_data:
```

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

Create `frontend/Dockerfile`:

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

CMD ["npm", "start"]
```

### Step 5.4: Run with Docker

```bash
# Build and start all services
docker-compose up --build

# Backend: http://localhost:8000
# Frontend: http://localhost:3000
# MongoDB: localhost:27017
```

### Step 5.5: Environment Variables

Create `frontend/.env`:

```env
REACT_APP_API_URL=http://localhost:8000/api/v1
```

Create production `.env.production`:

```env
REACT_APP_API_URL=https://your-api-domain.com/api/v1
```

---

## Bonus: Advanced Features {#bonus-advanced-features}

### Feature 1: Real-Time Updates with WebSockets

Add WebSocket support for live price updates:

```python
# backend/app/main.py
from fastapi import WebSocket
import asyncio

@app.websocket("/ws/portfolio/{portfolio_id}")
async def portfolio_websocket(websocket: WebSocket, portfolio_id: str):
    await websocket.accept()

    try:
        while True:
            # Fetch updated prices
            # Send to client
            await websocket.send_json({"prices": {...}})
            await asyncio.sleep(30)  # Update every 30 seconds
    except:
        await websocket.close()
```

### Feature 2: Portfolio Analytics

Add advanced analytics:
- Sharpe ratio calculation
- Beta calculation
- Correlation analysis
- Risk metrics

### Feature 3: Alerts and Notifications

Implement price alerts:
- Set target prices
- Email/SMS notifications
- Stop-loss alerts

### Feature 4: Export Features

Add export functionality:
- Export to CSV
- Generate PDF reports
- Excel exports with charts

### Feature 5: Social Features

- Share portfolios
- Follow other investors
- Discussion forums
- Paper trading

---

## Conclusion

Congratulations! You've built a complete Portfolio Management System with:

- **Backend**: FastAPI with yfinance integration
- **Frontend**: Modern React app with TypeScript
- **Features**: Real-time stock data, portfolio tracking, analytics
- **Deployment**: Docker-based deployment

### Next Steps

1. Add user authentication (JWT tokens)
2. Implement more advanced charts
3. Add dividend tracking
4. Build mobile app (React Native)
5. Add news integration
6. Implement AI-powered insights

### Resources

- [yfinance Documentation](https://pypi.org/project/yfinance/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Recharts Documentation](https://recharts.org/)

### Repository Structure

```
portfolio-management-system/
├── backend/               # Python FastAPI backend
├── frontend/             # React TypeScript frontend
├── docker-compose.yml    # Docker orchestration
└── README.md            # Project documentation
```

Happy coding! 🚀📈
