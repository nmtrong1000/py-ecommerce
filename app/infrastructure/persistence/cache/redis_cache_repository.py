import redis.asyncio as redis
from typing import Optional
import logging
from app.domain.repositories.cache_repository import CacheRepository

logger = logging.getLogger(__name__)


class RedisCacheRepository(CacheRepository):
  def __init__(self, client: redis.Redis):
    self.__client = client

  async def get(self, key: str) -> Optional[str]:
    value: bytes | None = await self.__client.get(key)
    logger.debug(f"[Redis] Cache hit: {key}")
    return value.decode("utf-8") if value is not None else None

  async def set(self, key: str, value: str, ttl: int | None = None):
    await self.__client.set(key, value.encode("utf-8"), ex=ttl)
    logger.debug(f"[Redis] Cache set: {key}")

  async def delete(self, key: str) -> None:
    await self.__client.delete(key)
    logger.debug(f"[Redis] Cache invalidate: {key}")

  async def delete_pattern(self, pattern: str) -> None:
    batch: list[bytes] = []

    async for key in self.__client.scan_iter(match=pattern, count=100):
      batch.append(key)
      if len(batch) >= 100:
        await self.__client.unlink(*batch)
        batch.clear()

    if batch:
      await self.__client.unlink(*batch)

    logger.debug(f"[Redis] Cache invalidate pattern: {pattern}")
