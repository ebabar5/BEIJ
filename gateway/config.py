from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Gateway configuration settings"""
    
    # Backend service configuration
    BACKEND_URL: str = "http://localhost:8001"
    BACKEND_TIMEOUT: int = 30
    
    # CORS configuration
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",  # React default
        "http://localhost:3001",  # React alternative
        "http://localhost:5173",  # Vite default
        "http://localhost:8080",  # Vue default
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
    
    # Gateway configuration
    GATEWAY_HOST: str = "0.0.0.0"
    GATEWAY_PORT: int = 8000
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Rate limiting (requests per minute)
    RATE_LIMIT: int = 100
    
    # Environment
    ENVIRONMENT: str = "development"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()

# Environment-specific overrides
if settings.ENVIRONMENT == "production":
    settings.ALLOWED_ORIGINS = [
        "https://your-frontend-domain.com",
        "https://www.your-frontend-domain.com"
    ]
    settings.LOG_LEVEL = "WARNING"
