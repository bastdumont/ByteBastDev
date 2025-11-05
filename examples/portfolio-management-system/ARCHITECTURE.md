# Portfolio Management System - Architecture

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER BROWSER                             │
│                     (http://localhost:3000)                     │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP/REST
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FRONTEND (React)                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Components (10)                                          │  │
│  │  - Dashboard, PortfolioDetail                            │  │
│  │  - PortfolioCard, HoldingsTable, PortfolioMetrics       │  │
│  │  - StockSearch, StockChart, AddHoldingForm              │  │
│  │  - CreatePortfolioForm, LoadingSpinner, ErrorMessage    │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  State Management                                         │  │
│  │  - React Query (TanStack Query)                          │  │
│  │  - Custom Hooks (15+)                                    │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Routing                                                  │  │
│  │  - React Router v6                                       │  │
│  │  - / → Dashboard                                         │  │
│  │  - /portfolio/:id → Portfolio Detail                    │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ axios HTTP requests
                             │ CORS enabled
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND API (FastAPI)                         │
│                  (http://localhost:8000/api/v1)                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  API Routes (14 endpoints)                                │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │  Stock Routes (/stocks)                            │  │  │
│  │  │  - GET /quote/{symbol}                             │  │  │
│  │  │  - GET /info/{symbol}                              │  │  │
│  │  │  - GET /history/{symbol}                           │  │  │
│  │  │  - GET /search?q={query}                           │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │  Portfolio Routes (/portfolios)                    │  │  │
│  │  │  - GET /                                           │  │  │
│  │  │  - POST /                                          │  │  │
│  │  │  - GET /{id}                                       │  │  │
│  │  │  - PUT /{id}                                       │  │  │
│  │  │  - DELETE /{id}                                    │  │  │
│  │  │  - POST /{id}/holdings                            │  │  │
│  │  │  - DELETE /{id}/holdings/{symbol}                 │  │  │
│  │  │  - POST /{id}/refresh                             │  │  │
│  │  │  - GET /{id}/metrics                              │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Services Layer                                           │  │
│  │  - StockService (yfinance integration)                   │  │
│  │  - PortfolioService (business logic)                     │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Models (Pydantic v2)                                     │  │
│  │  - Portfolio, StockHolding                               │  │
│  │  - PortfolioCreate, PortfolioUpdate                      │  │
│  │  - PyObjectId (custom MongoDB ID)                        │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────┬─────────────────────────────┬───────────────────┘
               │                             │
               │ Motor                       │ yfinance
               │ (async MongoDB)             │ (Yahoo Finance API)
               ▼                             ▼
┌──────────────────────────┐   ┌──────────────────────────────────┐
│  DATABASE (MongoDB)      │   │  EXTERNAL API                    │
│  (localhost:27017)       │   │  (Yahoo Finance)                 │
│  ┌────────────────────┐  │   │  - Stock quotes                  │
│  │ portfolio_db       │  │   │  - Historical data               │
│  │  - portfolios      │  │   │  - Company info                  │
│  │    collection      │  │   │  - Search results                │
│  └────────────────────┘  │   └──────────────────────────────────┘
└──────────────────────────┘
```

## 🔄 Data Flow

### Creating a Portfolio

```
User (Browser)
    ↓ clicks "New Portfolio"
Frontend: CreatePortfolioForm
    ↓ user fills form
    ↓ validates input
    ↓ calls useCreatePortfolio hook
React Query
    ↓ makes POST request
Axios API Client
    ↓ POST /api/v1/portfolios
Backend: FastAPI Router
    ↓ validates request
    ↓ calls PortfolioService
Service Layer
    ↓ creates Portfolio model
    ↓ saves to MongoDB
MongoDB
    ↓ returns saved document
Service Layer
    ↓ converts to Pydantic model
Backend API
    ↓ serializes response (id not _id)
Frontend
    ↓ receives portfolio data
React Query
    ↓ invalidates cache
    ↓ refetches portfolios list
UI Updates
    ↓ shows new portfolio card
User sees portfolio ✅
```

### Adding a Stock Holding

```
User
    ↓ searches for stock
StockSearch Component
    ↓ calls useStockSearch hook
    ↓ debounced search query
Backend: GET /stocks/search?q=AAPL
    ↓ calls yfinance
Yahoo Finance API
    ↓ returns search results
Frontend
    ↓ displays dropdown
User
    ↓ selects stock
    ↓ enters quantity, price, date
AddHoldingForm
    ↓ validates form
    ↓ calls useAddHolding hook
Backend: POST /portfolios/{id}/holdings
    ↓ validates holding data
    ↓ adds to portfolio.holdings array
    ↓ saves to MongoDB
Frontend
    ↓ invalidates portfolio cache
    ↓ refetches portfolio
HoldingsTable
    ↓ displays new holding
    ↓ calculates gains/losses
PortfolioMetrics
    ↓ updates total value
    ↓ shows performance
User sees updated portfolio ✅
```

### Viewing Stock Chart

```
User
    ↓ clicks stock symbol button
PortfolioDetail Page
    ↓ sets selectedStock state
    ↓ renders StockChart component
StockChart
    ↓ calls useStockHistory hook
React Query
    ↓ GET /stocks/history/AAPL?period=1mo
Backend
    ↓ calls yfinance
    ↓ fetches historical data
Yahoo Finance API
    ↓ returns price history
Backend
    ↓ formats data
Frontend
    ↓ receives historical prices
StockChart
    ↓ formats for Recharts
    ↓ renders LineChart
User sees interactive chart ✅
```

## 🔐 Authentication Flow (Current - Demo Mode)

```
Frontend Request
    ↓
API Endpoint
    ↓ checks for auth (deps.py)
Current User Dependency
    ↓ returns "demo_user" (hardcoded)
Route Handler
    ↓ uses user_id = "demo_user"
Service Layer
    ↓ filters by user_id
MongoDB Query
    ↓ db.portfolios.find({"user_id": "demo_user"})
Results
    ↓ returns user's portfolios
```

**Note**: All users currently share the same demo_user account.

## 📦 Component Hierarchy

### Frontend Component Tree

```
App (Router)
├── Dashboard Page
│   ├── Header
│   │   └── Create Portfolio Button
│   ├── CreatePortfolioForm (conditional)
│   └── Portfolio Grid
│       └── PortfolioCard (multiple)
│           ├── Portfolio Metrics
│           ├── Refresh Button
│           └── Delete Button
│
└── PortfolioDetail Page
    ├── Header
    │   ├── Back Button
    │   ├── Refresh Button
    │   └── Add Stock Button
    ├── PortfolioMetrics
    │   ├── Total Value Card
    │   ├── Total Cost Card
    │   ├── Gain/Loss Card
    │   ├── Return % Card
    │   └── Best/Worst Performers
    ├── AddHoldingForm (conditional)
    │   ├── StockSearch
    │   ├── Quantity Input
    │   ├── Price Input
    │   └── Date Picker
    ├── StockChart (conditional)
    │   └── Recharts LineChart
    └── HoldingsTable
        └── Holding Rows
            ├── Symbol
            ├── Quantity
            ├── Prices
            ├── Value
            ├── Gain/Loss
            └── Remove Button
```

## 🗄️ Database Schema

### MongoDB Collections

```javascript
// portfolios collection
{
  _id: ObjectId("..."),
  user_id: "demo_user",
  name: "Tech Stocks",
  description: "Technology investments",
  holdings: [
    {
      symbol: "AAPL",
      quantity: 10,
      purchase_price: 150.00,
      purchase_date: ISODate("2024-01-01T00:00:00Z"),
      current_price: 175.00  // updated on refresh
    }
  ],
  created_at: ISODate("2024-01-01T00:00:00Z"),
  updated_at: ISODate("2024-01-01T00:00:00Z")
}
```

### Indexes

```javascript
// portfolios collection indexes
db.portfolios.createIndex({ user_id: 1 })
db.portfolios.createIndex({ created_at: -1 })
db.portfolios.createIndex({ user_id: 1, created_at: -1 })
```

## 🔧 Technology Stack Details

### Frontend Stack
```
React 18.3.1
├── TypeScript 5.5.3
├── React Router 6.26.2
├── React Query 5.59.20
├── Axios 1.7.7
├── TailwindCSS 3.4.14
├── Recharts 2.13.3
└── date-fns 4.1.0
```

### Backend Stack
```
Python 3.11
├── FastAPI 0.104.1
├── Pydantic 2.9.2
├── Motor 3.3.2 (async MongoDB)
├── yfinance 0.2.32
└── uvicorn 0.24.0
```

### Infrastructure
```
Docker Compose
├── MongoDB 6.0
├── Node.js 18-alpine
└── Python 3.11-slim
```

## 🚀 Deployment Architecture

### Development (Current)
```
Docker Compose (Local)
├── pms-frontend:3000
├── pms-backend:8000
└── pms-mongodb:27017
```

### Production (Recommended)
```
Cloud Provider (AWS/GCP/Azure)
├── Frontend
│   ├── S3 + CloudFront (AWS)
│   └── Or: Vercel/Netlify
├── Backend
│   ├── ECS/EKS (AWS)
│   └── Load Balancer
├── Database
│   └── MongoDB Atlas
└── CDN
    └── CloudFront/CloudFlare
```

## 🔄 State Management

### React Query Cache Strategy

```
Query Keys:
- ['portfolios'] → All portfolios
- ['portfolio', id] → Single portfolio
- ['metrics', id] → Portfolio metrics
- ['stock-quote', symbol] → Stock quote
- ['stock-history', symbol, period] → Historical data
- ['stock-search', query] → Search results

Cache Times:
- Portfolios: 30s stale time
- Stock quotes: 60s stale + auto-refresh
- Stock history: 5min stale
- Search results: 5min stale

Invalidation:
- Create portfolio → invalidate ['portfolios']
- Update portfolio → invalidate ['portfolios'], ['portfolio', id]
- Add holding → invalidate ['portfolio', id], ['metrics', id]
- Remove holding → invalidate ['portfolio', id], ['metrics', id]
- Refresh prices → invalidate ['portfolio', id], ['metrics', id]
```

## 🔗 API Integration Points

### Internal APIs (Backend)
- Portfolio CRUD
- Holdings management
- Metrics calculation
- Price refresh

### External APIs
- Yahoo Finance (via yfinance)
  - Stock quotes
  - Historical prices
  - Company info
  - Stock search

### Future Integrations (Recommended)
- Alpha Vantage (stock data alternative)
- Finnhub (real-time data)
- News API (stock news)
- SendGrid (email notifications)
- Stripe (premium subscriptions)

## 📊 Performance Considerations

### Frontend Optimizations
- React Query caching
- Lazy loading ready
- Code splitting ready
- Memoized calculations
- Debounced search
- Optimistic updates

### Backend Optimizations
- Async/await throughout
- MongoDB indexes
- Connection pooling
- Response caching ready
- Batch operations ready

### Database Optimizations
- Indexed queries
- Projection (select specific fields)
- Lean queries (plain objects)
- Pagination ready

## 🔐 Security Layers

### Current Implementation
```
Frontend
└── API Client (axios)
    └── CORS headers

Backend
└── CORS middleware
    └── Allowed origins: localhost:3000

Database
└── Local MongoDB
    └── No authentication (dev mode)
```

### Production Requirements
```
Frontend
└── API Client
    └── JWT tokens in headers
    └── Secure cookies
    └── HTTPS only

Backend
└── CORS middleware
└── JWT validation
└── Rate limiting
└── Input sanitization
└── SQL injection prevention
└── XSS protection

Database
└── MongoDB Atlas
    └── Authentication
    └── Network isolation
    └── Encryption at rest
    └── IP whitelist
```

## 📈 Scalability Path

### Phase 1: Current (1-10 users)
- Single Docker Compose
- Local MongoDB
- No caching

### Phase 2: Small Scale (10-100 users)
- Deploy to single server
- MongoDB Atlas
- Redis caching
- CDN for frontend

### Phase 3: Medium Scale (100-1000 users)
- Load balancer
- Multiple backend instances
- Separate database server
- Object storage (S3)

### Phase 4: Large Scale (1000+ users)
- Kubernetes
- Horizontal scaling
- Database replication
- Microservices
- API gateway

---

**Architecture Version**: 1.0.0
**Last Updated**: November 2025
**Status**: Production Ready (with recommended enhancements)
