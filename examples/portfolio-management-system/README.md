# Portfolio Management System - Complete Example

This is a complete, production-ready example of a Portfolio Management System built with FastAPI, yfinance, React, and MongoDB.

## Features

- Real-time stock price tracking using yfinance
- Portfolio creation and management
- Stock holdings with gain/loss calculations
- Historical price charts
- Portfolio performance metrics
- RESTful API with FastAPI
- Modern React frontend with TypeScript
- MongoDB for data persistence
- Docker support for easy deployment

## Quick Start

### Option 1: Using Docker (Recommended)

```bash
# Clone and navigate to this directory
cd examples/portfolio-management-system

# Start all services with Docker Compose
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Manual Setup

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start MongoDB (if not using Docker)
# Make sure MongoDB is running on localhost:27017

# Run the backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

## Project Structure

```
portfolio-management-system/
├── backend/
│   ├── app/
│   │   ├── api/              # API routes
│   │   │   ├── stocks.py     # Stock endpoints
│   │   │   ├── portfolios.py # Portfolio endpoints
│   │   │   └── deps.py       # Dependencies
│   │   ├── models/           # Data models
│   │   │   ├── portfolio.py  # Portfolio models
│   │   │   └── user.py       # User models
│   │   ├── services/         # Business logic
│   │   │   ├── stock_service.py
│   │   │   └── portfolio_service.py
│   │   ├── config.py         # Configuration
│   │   └── main.py           # FastAPI app
│   ├── tests/                # Backend tests
│   ├── requirements.txt      # Python dependencies
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── portfolio/    # Portfolio components
│   │   │   └── stocks/       # Stock components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API services
│   │   ├── hooks/            # Custom React hooks
│   │   ├── types/            # TypeScript types
│   │   └── App.tsx           # Main app component
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml        # Docker orchestration
└── README.md
```

## API Endpoints

### Stock Endpoints

- `GET /api/v1/stocks/quote/{symbol}` - Get current stock price
- `GET /api/v1/stocks/info/{symbol}` - Get detailed stock information
- `GET /api/v1/stocks/history/{symbol}` - Get historical price data
- `GET /api/v1/stocks/search?q={query}` - Search for stocks
- `POST /api/v1/stocks/quotes` - Get multiple stock quotes

### Portfolio Endpoints

- `POST /api/v1/portfolios` - Create a new portfolio
- `GET /api/v1/portfolios` - Get all portfolios
- `GET /api/v1/portfolios/{id}` - Get portfolio by ID
- `PUT /api/v1/portfolios/{id}` - Update portfolio
- `DELETE /api/v1/portfolios/{id}` - Delete portfolio
- `POST /api/v1/portfolios/{id}/holdings` - Add stock holding
- `DELETE /api/v1/portfolios/{id}/holdings/{symbol}` - Remove holding
- `POST /api/v1/portfolios/{id}/refresh` - Refresh stock prices
- `GET /api/v1/portfolios/{id}/metrics` - Get portfolio metrics

## Environment Variables

### Backend (.env)

```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=portfolio_db
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (.env)

```env
REACT_APP_API_URL=http://localhost:8000/api/v1
```

## Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **yfinance** - Stock market data from Yahoo Finance
- **Motor** - Async MongoDB driver
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### Frontend
- **React** - UI library
- **TypeScript** - Type safety
- **TailwindCSS** - Styling
- **React Query** - Data fetching and caching
- **Recharts** - Charting library
- **React Router** - Routing

### Database
- **MongoDB** - NoSQL database for portfolio storage

## Usage Examples

### Create a Portfolio

```bash
curl -X POST http://localhost:8000/api/v1/portfolios \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tech Growth Portfolio",
    "description": "Focus on technology stocks"
  }'
```

### Get Stock Quote

```bash
curl http://localhost:8000/api/v1/stocks/quote/AAPL
```

### Add Stock Holding

```bash
curl -X POST http://localhost:8000/api/v1/portfolios/{portfolio_id}/holdings \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "quantity": 10,
    "purchase_price": 150.00,
    "purchase_date": "2024-01-01T00:00:00Z"
  }'
```

## Development

### Running Tests

```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
cd frontend
npm test
```

### Code Formatting

```bash
# Backend
cd backend
black app/
isort app/

# Frontend
cd frontend
npm run lint
npm run format
```

## Deployment

### Production Deployment with Docker

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Start services
docker-compose -f docker-compose.prod.yml up -d
```

### Environment Setup for Production

1. Update `.env` files with production values
2. Change `SECRET_KEY` to a secure random string
3. Update `MONGODB_URL` to production database
4. Set `REACT_APP_API_URL` to production API URL
5. Configure CORS origins in backend config

## Features in Detail

### Real-Time Stock Data
- Fetches live stock prices using yfinance
- Supports historical data retrieval
- Multiple time periods and intervals
- Company information and metrics

### Portfolio Management
- Create multiple portfolios
- Track stock holdings
- Calculate gains/losses
- Portfolio performance metrics
- Real-time price updates

### Analytics
- Total invested amount
- Current portfolio value
- Gain/loss calculations
- Percentage returns
- Per-stock performance

### User Interface
- Responsive design
- Interactive charts
- Stock search functionality
- Real-time updates
- Portfolio dashboard

## Troubleshooting

### Backend Issues

**MongoDB Connection Error**
- Ensure MongoDB is running: `mongod --version`
- Check connection string in `.env`
- Verify firewall settings

**yfinance Data Not Loading**
- Check internet connection
- Some stocks may have limited data
- Try different time periods

### Frontend Issues

**API Connection Error**
- Verify backend is running on port 8000
- Check `REACT_APP_API_URL` in `.env`
- Check browser console for CORS errors

**Charts Not Rendering**
- Ensure historical data is available
- Check browser console for errors
- Verify Recharts is installed

## Future Enhancements

- [ ] User authentication with JWT
- [ ] Dividend tracking
- [ ] Portfolio comparison
- [ ] News integration
- [ ] Price alerts
- [ ] Export to CSV/PDF
- [ ] Mobile app (React Native)
- [ ] AI-powered insights
- [ ] Social features (follow portfolios)
- [ ] Paper trading mode

## Contributing

This is an example project for learning purposes. Feel free to:
- Fork and modify
- Add new features
- Submit improvements
- Report issues

## License

MIT License - Feel free to use this example for your own projects.

## Resources

- [yfinance Documentation](https://pypi.org/project/yfinance/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [MongoDB Documentation](https://www.mongodb.com/docs/)
- [Tutorial](../../tutorials/portfolio-management-system-tutorial.md)

## Support

For questions or issues related to this example:
1. Check the [complete tutorial](../../tutorials/portfolio-management-system-tutorial.md)
2. Review the inline code comments
3. Check API documentation at http://localhost:8000/docs
4. Consult the resources above

---

**Built with ❤️ for ByteClaude Framework**
