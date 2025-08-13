"""
Logging Configuration
"""
import logging
import sys
from typing import Dict, Any
from app.core.config import settings

def setup_logging() -> None:
    """Setup application logging"""
    
    # Configure root logger
    logging.basicConfig(
        level=logging.DEBUG if settings.DEBUG else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set specific logger levels
    loggers = {
        "uvicorn": logging.INFO,
        "uvicorn.error": logging.INFO,
        "uvicorn.access": logging.INFO if settings.DEBUG else logging.WARNING,
        "fastapi": logging.INFO,
        "httpx": logging.WARNING,
        "transformers": logging.WARNING,
        "torch": logging.WARNING,
    }
    
    for logger_name, level in loggers.items():
        logging.getLogger(logger_name).setLevel(level)

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance"""
    return logging.getLogger(name)
