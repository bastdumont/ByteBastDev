# FastAPI Backend

Production-ready FastAPI backend with MongoDB, JWT authentication, and async operations.

## Features

- ✅ **FastAPI** framework with async/await
- ✅ **MongoDB** with Motor (async driver)
- ✅ **JWT Authentication** with refresh tokens
- ✅ **Role-based access control** (RBAC)
- ✅ **Pydantic V2** for validation
- ✅ **Automatic API documentation** (Swagger/ReDoc)
- ✅ **CORS** configuration
- ✅ **Environment-based settings**
- ✅ **Structured logging**
- ✅ **Error handling middleware**
- ✅ **Health check endpoint**
- ✅ **Testing with pytest**

## Quick Start

### Prerequisites

- Python 3.11+
- MongoDB 5.0+

### Installation

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```bash
cp .env.example .env
```

4. Update `.env` with your configuration:
```env
PROJECT_NAME="{{project_name}}"
MONGODB_URL="mongodb://localhost:27017"
DATABASE_NAME="{{database_name}}"
SECRET_KEY="your-secret-key-here"
```

5. Run the server:
```bash
uvicorn app.main:app --reload
```

6. Open [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs) for API documentation.

## Project Structure

```
app/
├── main.py                 # Application entry point
├── api/                    # API routes
│   ├── routes.py          # Router aggregation
│   ├── auth.py            # Authentication endpoints
│   ├── users.py           # User endpoints
│   └── ...
├── core/                   # Core functionality
│   ├── config.py          # Settings
│   ├── database.py        # Database connection
│   ├── security.py        # JWT and password utilities
│   └── dependencies.py    # FastAPI dependencies
├── models/                 # Database models
│   ├── user.py
│   └── ...
├── schemas/                # Pydantic schemas
│   ├── user.py
│   ├── auth.py
│   └── ...
├── services/               # Business logic
│   ├── user_service.py
│   ├── auth_service.py
│   └── ...
├── utils/                  # Utility functions
│   └── ...
└── middleware/             # Custom middleware
    ├── error_handler.py
    └── logging.py

tests/                      # Test suite
├── conftest.py
├── test_auth.py
└── ...
```

## API Endpoints

### Authentication

- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/refresh` - Refresh access token
- `GET /api/v1/auth/me` - Get current user

### Users

- `GET /api/v1/users` - List users (admin only)
- `GET /api/v1/users/{id}` - Get user by ID
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user (admin only)

### Health

- `GET /health` - Health check
- `GET /` - API information

## Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. Register or login to get access and refresh tokens
2. Include access token in requests:
   ```
   Authorization: Bearer <access_token>
   ```
3. Use refresh token to get new access token when expired

### Example: Register User

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword",
    "name": "John Doe"
  }'
```

### Example: Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword"
  }'
```

Response:
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

### Example: Authenticated Request

```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer <access_token>"
```

## Database

### MongoDB Connection

The application uses Motor (async MongoDB driver) for database operations:

```python
from app.core.database import get_database

db = get_database()
users = await db.users.find().to_list(length=100)
```

### Models

Define models using Pydantic:

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class User(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    email: str
    name: str
    role: str = "user"
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

## Testing

Run tests with pytest:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

## Development

### Code Formatting

```bash
# Format code with Black
black .

# Lint with Ruff
ruff check .

# Type check with mypy
mypy app
```

### Environment Variables

All configuration is managed through environment variables:

```env
# Application
PROJECT_NAME="My API"
VERSION="1.0.0"
ENVIRONMENT="development"

# Security
SECRET_KEY="your-secret-key"
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Database
MONGODB_URL="mongodb://localhost:27017"
DATABASE_NAME="mydb"

# CORS
CORS_ORIGINS=["http://localhost:3000"]

# Logging
LOG_LEVEL="INFO"
```

## Deployment

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t my-api .
docker run -p 8000:8000 my-api
```

### Production

For production deployment:

1. Set environment to production:
```env
ENVIRONMENT="production"
```

2. Use production-ready server:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

3. Use a reverse proxy (nginx/Caddy)

4. Enable HTTPS

5. Set up monitoring and logging

## Middleware

### Error Handler

Catches and formats all exceptions:

```python
@app.middleware("http")
async def error_handler_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        # Handle error
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )
```

### Logging

Logs all requests:

```python
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    # Log request
    response = await call_next(request)
    # Log response
    return response
```

## Security Best Practices

- ✅ Passwords are hashed with bcrypt
- ✅ JWT tokens for authentication
- ✅ CORS properly configured
- ✅ Environment variables for secrets
- ✅ Input validation with Pydantic
- ✅ SQL injection prevention (MongoDB)
- ✅ Rate limiting (implement with slowapi)

## Performance Tips

1. **Use async/await** throughout
2. **Database indexing** for common queries
3. **Caching** with Redis for frequently accessed data
4. **Connection pooling** for database
5. **Pagination** for large datasets
6. **Background tasks** for slow operations

## Monitoring

Add monitoring with:

- **Prometheus** for metrics
- **Grafana** for dashboards
- **Sentry** for error tracking
- **ELK Stack** for log aggregation

## License

MIT License - use freely for your projects.

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Motor Documentation](https://motor.readthedocs.io/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [MongoDB Documentation](https://www.mongodb.com/docs/)
