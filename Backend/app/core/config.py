"""
Application Configuration Management
"""
import os
from typing import List, Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""

    # Application
    PROJECT_NAME: str = "LinkedIn AI Agent Backend"
    VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15

    # CORS
    ALLOWED_HOSTS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "https://*.hf.space",
        "https://*.huggingface.co"
    ]
    CORS_ORIGINS: Optional[str] = os.getenv("CORS_ORIGINS")

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Supabase
    SUPABASE_URL: Optional[str] = os.getenv("SUPABASE_URL")
    SUPABASE_ANON_KEY: Optional[str] = os.getenv("SUPABASE_ANON_KEY")
    SUPABASE_SERVICE_KEY: Optional[str] = os.getenv("SUPABASE_SERVICE_KEY")

    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    REDIS_MAX_CONNECTIONS: int = int(os.getenv("REDIS_MAX_CONNECTIONS", "20"))
    REDIS_TIMEOUT: int = int(os.getenv("REDIS_TIMEOUT", "10"))

    # AI Models
    HF_HOME: str = os.getenv("HF_HOME", "/app/models")
    TRANSFORMERS_CACHE: str = os.getenv("TRANSFORMERS_CACHE", "/app/models")
    TORCH_HOME: str = os.getenv("TORCH_HOME", "/app/models")

    GPT_OSS_MODEL: str = os.getenv("GPT_OSS_MODEL", "microsoft/DialoGPT-medium")
    QWEN_MODEL: str = os.getenv("QWEN_MODEL", "Qwen/Qwen-VL-Chat")

    # OpenAI API (for production AI features)
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4")

    # OpenRouter API (for image generation and content)
    OPENROUTER_API_KEY: Optional[str] = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_BASE_URL: str = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

    # Rate Limiting
    RATE_LIMIT_DEFAULT: int = int(os.getenv("RATE_LIMIT_DEFAULT", "100"))
    RATE_LIMIT_AUTH: int = int(os.getenv("RATE_LIMIT_AUTH", "5"))
    RATE_LIMIT_AI: int = int(os.getenv("RATE_LIMIT_AI", "20"))

    # LinkedIn API (for future use)
    LINKEDIN_CLIENT_ID: Optional[str] = os.getenv("LINKEDIN_CLIENT_ID")
    LINKEDIN_CLIENT_SECRET: Optional[str] = os.getenv("LINKEDIN_CLIENT_SECRET")

    # Monitoring
    ENABLE_METRICS: bool = os.getenv("ENABLE_METRICS", "true").lower() == "true"
    SENTRY_DSN: Optional[str] = os.getenv("SENTRY_DSN")

    # Hugging Face Spaces
    HUGGING_FACE_SPACE: bool = os.getenv("SPACE_ID") is not None
    SPACE_ID: Optional[str] = os.getenv("SPACE_ID")

    class Config:
        env_file = ".env"
        case_sensitive = True

# Create global settings instance
settings = Settings()
