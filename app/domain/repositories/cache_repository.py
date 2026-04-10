from abc import ABC, abstractmethod
from typing import Optional


class CacheRepository(ABC):
  async def get(self, key: str) -> Optional[str]:
    pass

  @abstractmethod
  async def set(self, key: str, value: str, ttl: int | None = None) -> None:
    pass

  @abstractmethod
  async def delete(self, key: str) -> None:
    pass

  @abstractmethod
  async def delete_pattern(self, pattern: str) -> None:
    pass
