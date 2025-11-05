from pydantic_settings import BaseSettings
from typing import List
from pydantic import field_validator
import json

class Settings(BaseSettings):
    """Application settings"""

    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Portfolio Management System"
    VERSION: str = "1.0.0"

    # Database
    MONGODB_URL: str = "mongodb://mongodb:27017"
    DATABASE_NAME: str = "portfolio_db"

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list"""
        if isinstance(v, str):
            # Try to parse as JSON first
            if v.startswith("["):
                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    pass
            # Otherwise treat as single URL
            return [v]
        return v

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
