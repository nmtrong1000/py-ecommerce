from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional, List
from app.domain.entities.media_entity import Media, MediaListResult


class MediaRepository(ABC):
  @abstractmethod
  async def create(self, media: Media) -> Media:
    pass

  @abstractmethod
  async def get(self, media_id: UUID) -> Optional[Media]:
    pass

  @abstractmethod
  async def list(
    self, page: int, page_size: int, filters: dict, sort_by: str, sort_order: str
  ) -> MediaListResult:
    pass

  @abstractmethod
  async def update(self, media: Media) -> Media:
    pass

  @abstractmethod
  async def delete(self, media_ids: List[UUID]) -> bool:
    pass
