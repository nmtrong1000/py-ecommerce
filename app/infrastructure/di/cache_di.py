from app.domain.repositories.cache_repository import CacheRepository
from app.infrastructure.persistence.cache.redis_cache_repository import (
  RedisCacheRepository,
)
from app.infrastructure.persistence.cache.redis_client import get_redis_client


def get_cache_repository() -> CacheRepository:
  redis_client = get_redis_client()
  return RedisCacheRepository(redis_client)
