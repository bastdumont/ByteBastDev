# Quick Start Guide - Portfolio Management System

Get your Portfolio Management System up and running in minutes!

## Prerequisites

- Python 3.9+ installed
- Node.js 18+ installed
- MongoDB installed (or use Docker)
- Git installed

## Option 1: Docker Quick Start (Easiest) 🚀

```bash
# 1. Clone or copy this template
cd my-portfolio-app

# 2. Start everything with one command
docker-compose up --build

# 3. Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

That's it! Your portfolio management system is now running.

## Option 2: Manual Setup

### Step 1: Backend Setup (5 minutes)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Start the backend (make sure MongoDB is running)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend is now running at http://localhost:8000

### Step 2: Frontend Setup (5 minutes)

Open a new terminal:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Start the development server
npm start
```

Frontend is now running at http://localhost:3000

### Step 3: MongoDB Setup

**Option A: Using Docker**
```bash
docker run -d -p 27017:27017 --name mongodb mongo:7.0
```

**Option B: Local Installation**
```bash
# Start MongoDB
mongod

# Or on macOS with Homebrew:
brew services start mongodb-community
```

## First Steps After Setup

### 1. Test the API

Visit http://localhost:8000/docs to see interactive API documentation.

Try this in your browser or curl:
```bash
curl http://localhost:8000/api/v1/stocks/quote/AAPL
```

### 2. Create Your First Portfolio

1. Open http://localhost:3000 in your browser
2. Click "Create Portfolio"
3. Enter a name like "My First Portfolio"
4. Click "Create"

### 3. Add Stock Holdings

1. Open your portfolio
2. Click "Add Holding"
3. Search for a stock (e.g., "AAPL")
4. Enter quantity and purchase details
5. Click "Add"

### 4. View Portfolio Performance

Your portfolio will automatically:
- Fetch current stock prices
- Calculate gains/losses
- Display performance metrics
- Show interactive charts

## Common Commands

```bash
# Start all services with Docker
docker-compose up

# Stop all services
docker-compose down

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Rebuild after code changes
docker-compose up --build

# Run backend tests
cd backend && pytest tests/

# Run frontend tests
cd frontend && npm test
```

## Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.9+

# Check MongoDB is running
mongosh  # Should connect

# Check port 8000 is free
lsof -i :8000
```

### Frontend won't start
```bash
# Check Node version
node --version  # Should be 18+

# Clear npm cache
npm cache clean --force
rm -rf node_modules package-lock.json
npm install

# Check port 3000 is free
lsof -i :3000
```

### Can't connect to API
- Check backend is running: http://localhost:8000/health
- Check CORS settings in backend/.env
- Verify REACT_APP_API_URL in frontend/.env

### MongoDB connection error
- Ensure MongoDB is running
- Check MONGODB_URL in backend/.env
- Try: `mongosh` to test connection

## Next Steps

1. **Read the Tutorial**: See `../../tutorials/portfolio-management-system-tutorial.md` for detailed explanations

2. **Explore the Code**:
   - Backend API: `backend/app/api/`
   - Stock Service: `backend/app/services/stock_service.py`
   - React Components: `frontend/src/components/`
   - API Client: `frontend/src/services/api.ts`

3. **Customize**:
   - Update theme colors in `frontend/tailwind.config.js`
   - Add new API endpoints in `backend/app/api/`
   - Create new React components in `frontend/src/components/`

4. **Add Features**:
   - User authentication
   - Price alerts
   - News integration
   - Portfolio comparison
   - Export to CSV/PDF

5. **Deploy**:
   - Set up production environment variables
   - Configure proper security settings
   - Use managed MongoDB (Atlas)
   - Deploy to cloud platform

## Useful Endpoints

- **Health Check**: http://localhost:8000/health
- **API Documentation**: http://localhost:8000/docs
- **OpenAPI Spec**: http://localhost:8000/api/v1/openapi.json
- **Frontend**: http://localhost:3000

## Getting Help

1. Check the complete tutorial for detailed guidance
2. Review the example project for working code
3. Visit API docs for endpoint documentation
4. Check FastAPI and React documentation

## Example API Calls

```bash
# Get stock quote
curl http://localhost:8000/api/v1/stocks/quote/AAPL

# Get stock info
curl http://localhost:8000/api/v1/stocks/info/AAPL

# Get historical data
curl "http://localhost:8000/api/v1/stocks/history/AAPL?period=1mo&interval=1d"

# Search stocks
curl "http://localhost:8000/api/v1/stocks/search?q=apple"

# Create portfolio (after adding auth)
curl -X POST http://localhost:8000/api/v1/portfolios \
  -H "Content-Type: application/json" \
  -d '{"name": "Tech Portfolio", "description": "My tech stocks"}'
```

## Environment Configuration

### Backend .env
```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=portfolio_db
SECRET_KEY=change-this-secret-key
BACKEND_CORS_ORIGINS=http://localhost:3000
```

### Frontend .env
```env
REACT_APP_API_URL=http://localhost:8000/api/v1
```

## Performance Tips

1. **Cache Stock Data**: yfinance has rate limits, implement caching
2. **Batch Requests**: Fetch multiple stocks at once
3. **Optimize Queries**: Use MongoDB indexes
4. **Lazy Loading**: Load charts on demand
5. **WebSockets**: For real-time updates (advanced)

## Security Checklist

Before deploying to production:

- [ ] Change SECRET_KEY to a strong random value
- [ ] Enable HTTPS
- [ ] Add authentication
- [ ] Configure CORS properly
- [ ] Use environment variables for secrets
- [ ] Enable MongoDB authentication
- [ ] Set up rate limiting
- [ ] Add input validation
- [ ] Implement logging and monitoring
- [ ] Regular security updates

---

**Happy Portfolio Building! 📈**

For detailed explanations, see the complete tutorial at:
`../../tutorials/portfolio-management-system-tutorial.md`
