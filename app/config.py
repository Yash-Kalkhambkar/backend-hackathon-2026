# Configuration settings loaded from .env file
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    DATABASE_URL: str
    GROQ_API_KEY: str
    
    class Config:
        env_file = ".env"


# Global settings instance
settings = Settings()
