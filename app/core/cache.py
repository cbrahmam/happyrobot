from functools import wraps
from typing import Optional
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache as fastapi_cache
from redis import asyncio as aioredis
from ..config import settings

async def setup_cache():
    """Initialize Redis cache"""
    redis = aioredis.from_url(
        settings.REDIS_URL,
        encoding="utf8",
        decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="loadchecker-cache")

def cache(expire: Optional[int] = None):
    """
    Cache decorator that uses Redis backend
    Args:
        expire: Cache expiration time in seconds
    """
    def decorator(func):
        @wraps(func)
        @fastapi_cache(
            expire=expire or settings.CACHE_EXPIRATION
        )
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        return wrapper
    return decorator