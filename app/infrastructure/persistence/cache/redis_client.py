import redis.asyncio as redis
from app.infrastructure.config.settings import settings

_redis_client: redis.Redis | None = None


def get_redis_client() -> redis.Redis:
  global _redis_client

  if _redis_client is None:
    _redis_client = redis.Redis(
      host=settings.REDIS_HOST,
      port=settings.REDIS_PORT,
      db=settings.REDIS_DB,
      password=settings.REDIS_PASSWORD,
      decode_responses=False,
    )

  return _redis_client
