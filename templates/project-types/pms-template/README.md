# Portfolio Management System Template

This template provides a complete, production-ready Portfolio Management System for tracking stock portfolios with real-time market data.

## What's Included

- **Backend**: FastAPI + Python + yfinance for stock data
- **Frontend**: React + TypeScript + TailwindCSS
- **Database**: MongoDB for portfolio storage
- **Docker**: Complete containerization setup
- **Testing**: Test suites for both backend and frontend
- **Documentation**: Comprehensive API docs and tutorial

## Quick Start

### Using ByteClaude Framework

```bash
# Use the framework to generate the project
python orchestrator/main.py --task "Create a portfolio management system using the PMS template"
```

### Manual Setup

1. **Copy Template**
```bash
cp -r templates/project-types/pms-template my-portfolio-app
cd my-portfolio-app
```

2. **Install Dependencies**
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

3. **Configure Environment**
```bash
# Backend
cp backend/.env.example backend/.env
# Edit backend/.env with your settings

# Frontend
cp frontend/.env.example frontend/.env
# Edit frontend/.env with your settings
```

4. **Run with Docker (Recommended)**
```bash
docker-compose up --build
```

Or run manually:

```bash
# Terminal 1 - MongoDB
mongod

# Terminal 2 - Backend
cd backend
uvicorn app.main:app --reload

# Terminal 3 - Frontend
cd frontend
npm start
```

5. **Access Application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Features

### Core Features
✅ Real-time stock price tracking with yfinance
✅ Portfolio creation and management
✅ Stock holdings with gain/loss calculations
✅ Historical price charts and visualizations
✅ Portfolio performance metrics
✅ Stock search functionality
✅ RESTful API with automatic documentation
✅ Responsive, modern UI

### Technical Features
✅ FastAPI backend with async support
✅ React with TypeScript for type safety
✅ TailwindCSS for styling
✅ React Query for data fetching and caching
✅ MongoDB for flexible data storage
✅ Docker support for easy deployment
✅ Comprehensive error handling
✅ API rate limiting and caching

## Project Structure

```
{{project_name}}/
├── backend/
│   ├── app/
│   │   ├── api/              # API routes
│   │   ├── models/           # Data models
│   │   ├── services/         # Business logic
│   │   ├── config.py         # Configuration
│   │   └── main.py           # FastAPI app
│   ├── tests/                # Backend tests
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API services
│   │   ├── hooks/            # Custom hooks
│   │   └── types/            # TypeScript types
│   └── package.json
├── docker-compose.yml
└── README.md
```

## Customization Options

### Theme
- Light mode (default)
- Dark mode
- Auto (system preference)

### Stock Data Provider
- yfinance (default, free)
- Alpha Vantage (requires API key)
- Finnhub (requires API key)

### Authentication
- None (default)
- JWT tokens
- OAuth2

### Chart Library
- Recharts (default)
- Chart.js
- Plotly

## Environment Variables

### Backend (.env)
```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME={{mongodb_database}}
SECRET_KEY=your-secret-key
BACKEND_CORS_ORIGINS=http://localhost:{{frontend_port}}
```

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:{{api_port}}/api/v1
```

## API Endpoints

### Stocks
- `GET /api/v1/stocks/quote/{symbol}` - Get stock quote
- `GET /api/v1/stocks/info/{symbol}` - Get stock info
- `GET /api/v1/stocks/history/{symbol}` - Get price history
- `GET /api/v1/stocks/search` - Search stocks
- `POST /api/v1/stocks/quotes` - Get multiple quotes

### Portfolios
- `POST /api/v1/portfolios` - Create portfolio
- `GET /api/v1/portfolios` - List portfolios
- `GET /api/v1/portfolios/{id}` - Get portfolio
- `PUT /api/v1/portfolios/{id}` - Update portfolio
- `DELETE /api/v1/portfolios/{id}` - Delete portfolio
- `POST /api/v1/portfolios/{id}/holdings` - Add holding
- `DELETE /api/v1/portfolios/{id}/holdings/{symbol}` - Remove holding
- `POST /api/v1/portfolios/{id}/refresh` - Refresh prices
- `GET /api/v1/portfolios/{id}/metrics` - Get metrics

## Testing

```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
cd frontend
npm test

# Run with coverage
pytest tests/ --cov=app
npm test -- --coverage
```

## Deployment

### Docker Deployment (Recommended)

```bash
# Production build
docker-compose -f docker-compose.prod.yml up --build -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Manual Deployment

1. **Backend**
```bash
cd backend
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

2. **Frontend**
```bash
cd frontend
npm run build
# Serve build/ directory with nginx or similar
```

## Common Issues

### yfinance Rate Limits
- Implement caching for frequently accessed data
- Use batch requests when possible
- Consider upgrading to paid data provider for production

### MongoDB Connection
- Ensure MongoDB is running and accessible
- Check connection string in .env
- Verify network/firewall settings

### CORS Errors
- Update BACKEND_CORS_ORIGINS in backend/.env
- Ensure frontend URL matches exactly

## Resources

- **Complete Tutorial**: See `../../tutorials/portfolio-management-system-tutorial.md`
- **Full Example**: See `../../examples/portfolio-management-system/`
- **API Documentation**: http://localhost:{{api_port}}/docs
- **yfinance Docs**: https://pypi.org/project/yfinance/
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **React Docs**: https://react.dev/

## Next Steps

1. **Follow the Tutorial**: Complete step-by-step guide in the tutorials folder
2. **Add Authentication**: Implement JWT or OAuth2 for user management
3. **Enhance UI**: Customize theme and add more visualizations
4. **Add Features**:
   - Price alerts
   - Dividend tracking
   - News integration
   - Portfolio comparison
   - Export to CSV/PDF
5. **Deploy**: Deploy to production with proper security
6. **Mobile App**: Create mobile version with React Native

## Support

- Check the complete tutorial for detailed explanations
- Review the example project for working code
- Visit API documentation for endpoint details
- Consult framework documentation for integration

## License

This template is part of the ByteClaude Framework and is licensed under MIT License.

---

**Built for ByteClaude Framework** | Template Version {{version}}
