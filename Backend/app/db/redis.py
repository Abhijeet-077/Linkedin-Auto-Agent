"""
Redis Cache Integration
"""
import json
import asyncio
from typing import Optional, Any, Dict
import redis.asyncio as redis
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)

class RedisClient:
    """Redis cache client"""
    
    def __init__(self):
        self.client: Optional[redis.Redis] = None
        
    async def connect(self) -> None:
        """Initialize Redis connection"""
        try:
            self.client = redis.from_url(
                settings.REDIS_URL,
                max_connections=settings.REDIS_MAX_CONNECTIONS,
                socket_timeout=settings.REDIS_TIMEOUT,
                decode_responses=True
            )
            
            # Test connection
            await self.client.ping()
            logger.info("✅ Redis connection established")
        except Exception as e:
            logger.warning(f"⚠️ Redis connection failed: {e}, using in-memory cache")
            self.client = None
    
    async def disconnect(self) -> None:
        """Close Redis connection"""
        if self.client:
            await self.client.close()
            logger.info("Redis connection closed")
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.client:
            return None
            
        try:
            value = await self.client.get(key)
            return json.loads(value) if value else None
        except Exception as e:
            logger.error(f"Redis get error: {e}")
            return None
    
    async def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        """Set value in cache"""
        if not self.client:
            return False
            
        try:
            await self.client.setex(key, expire, json.dumps(value))
            return True
        except Exception as e:
            logger.error(f"Redis set error: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete key from cache"""
        if not self.client:
            return False
            
        try:
            await self.client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Redis delete error: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        if not self.client:
            return False
            
        try:
            return bool(await self.client.exists(key))
        except Exception as e:
            logger.error(f"Redis exists error: {e}")
            return False

# Global instance
redis_client = RedisClient()

async def init_redis() -> None:
    """Initialize Redis connection"""
    await redis_client.connect()

async def get_redis() -> RedisClient:
    """Get Redis client instance"""
    return redis_client
