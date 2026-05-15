"""
Configuration Management
Handles environment-based configuration using Pydantic Settings
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
import os
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    Supports .env file for local development
    """
    
    # App Settings
    APP_NAME: str = Field(default="Legal Recon", description="Application name")
    APP_VERSION: str = Field(default="0.1.0", description="Application version")
    DEBUG: bool = Field(default=False, description="Debug mode")
    ENVIRONMENT: str = Field(default="development", description="Environment: development, staging, production")
    
    # Server Settings
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    WORKERS: int = Field(default=1, description="Number of worker processes")
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FILE: str = Field(default="logs/app.log", description="Log file path")
    
    # FastAPI Settings
    OPENAPI_URL: str = Field(default="/api/openapi.json", description="OpenAPI schema URL")
    DOCS_URL: str = Field(default="/api/docs", description="API documentation URL")
    REDOC_URL: str = Field(default="/api/redoc", description="ReDoc documentation URL")
    
    # CORS Settings
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080"],
        description="Allowed CORS origins"
    )
    CORS_CREDENTIALS: bool = Field(default=True, description="Allow CORS credentials")
    CORS_METHODS: List[str] = Field(default=["*"], description="Allowed CORS methods")
    CORS_HEADERS: List[str] = Field(default=["*"], description="Allowed CORS headers")
    
    # NLP Settings
    NLP_MODEL_PATH: str = Field(default="models/", description="Path to NLP models")
    URDU_TOKENIZER_PATH: str = Field(default="models/urdu_tokenizer", description="Urdu tokenizer path")
    NER_MODEL_PATH: str = Field(default="models/ner_model", description="NER model path")
    
    # Database Settings (Future)
    DATABASE_URL: str = Field(
        default="sqlite:///./legal_recon.db",
        description="Database connection URL"
    )
    
    # Processing Settings
    MAX_TEXT_LENGTH: int = Field(default=50000, description="Maximum text length for processing")
    PROCESSING_TIMEOUT: int = Field(default=300, description="Processing timeout in seconds")
    
    # API Settings
    API_V1_PREFIX: str = Field(default="/api/v1", description="API v1 prefix")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings (cached)
    Uses dependency injection in FastAPI
    """
    return Settings()
