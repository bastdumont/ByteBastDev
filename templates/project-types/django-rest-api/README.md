# Django REST API

Production-ready Django REST Framework API with PostgreSQL, JWT authentication, and comprehensive documentation.

## Overview

A complete REST API built with Django featuring:
- **Django REST Framework**: Powerful web API framework
- **PostgreSQL**: Robust database
- **JWT Authentication**: Token-based security
- **Admin Panel**: Built-in Django admin
- **API Documentation**: Auto-generated docs
- **Pagination**: Built-in support
- **Filtering**: Advanced filtering capabilities

## Features

✅ **REST API**
- RESTful endpoints
- JSON serialization
- Content negotiation
- Request/response validation

✅ **Authentication & Permissions**
- JWT tokens
- Role-based access control
- Custom permissions
- Token refresh

✅ **Database**
- PostgreSQL integration
- Django ORM
- Migrations
- Query optimization

✅ **Documentation**
- Swagger/OpenAPI
- Auto-generated docs
- API schema

✅ **Development**
- Django admin panel
- Shell REPL
- Management commands
- Testing framework

## Quick Start

### Prerequisites
```bash
Python >= 3.11
PostgreSQL >= 14
pip >= 23.0
```

### Installation

```bash
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Access
- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/
- Docs: http://localhost:8000/api/schema/

## Project Structure

```
django-rest-api/
├── manage.py
├── requirements.txt
├── config/
│   ├── settings.py        # Configuration
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI config
├── apps/
│   └── users/
│       ├── models.py      # Data models
│       ├── serializers.py # API serializers
│       ├── views.py       # API views
│       ├── urls.py        # Routes
│       └── tests.py       # Tests
└── README.md
```

## API Examples

### Register User
```bash
POST /api/auth/register
{
  "email": "user@example.com",
  "password": "secure_password",
  "name": "John Doe"
}
```

### Login
```bash
POST /api/auth/login
{
  "email": "user@example.com",
  "password": "secure_password"
}

Response:
{
  "access": "eyJ...",
  "refresh": "eyJ..."
}
```

### Get Users
```bash
GET /api/users/?page=1&page_size=10
Authorization: Bearer {access_token}
```

## Database

### Create Models

```python
from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
```

### Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Configuration

### Environment Variables

```bash
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/api
ALLOWED_HOSTS=localhost,127.0.0.1
JWT_SECRET=your-jwt-secret
```

### Settings

```python
# config/settings.py
INSTALLED_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'apps.users',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

## Development

### Commands

```bash
python manage.py shell          # Python REPL
python manage.py createsuperuser # Create admin
python manage.py makemigrations  # Create migrations
python manage.py migrate         # Apply migrations
python manage.py test           # Run tests
python manage.py collectstatic  # Collect static files
```

### Testing

```bash
python manage.py test apps.users
python manage.py test --keepdb  # Reuse test database
```

## Deployment

### Production Settings

```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "config.wsgi:application"]
```

## Security

✅ CSRF protection  
✅ SQL injection prevention  
✅ XSS protection  
✅ Rate limiting ready  
✅ HTTPS/SSL support  
✅ Password hashing  

## Performance

- Query optimization with `select_related()`, `prefetch_related()`
- Database indexing
- Caching support
- Pagination built-in
- Async support with Django 3.1+

## Troubleshooting

### Database Error

```bash
python manage.py migrate --fake-initial
python manage.py migrate
```

### Permission Denied

Check user permissions:
```bash
python manage.py shell
>>> from django.contrib.auth.models import User
>>> user = User.objects.get(username='admin')
>>> user.has_perm('app.view_model')
```

---

**Ready to build your API!** 🚀
