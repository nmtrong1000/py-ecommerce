from typing import Optional, List
from uuid import uuid4, UUID

from app.domain.entities.media_entity import Media, MediaListResult
from app.domain.repositories.media_repository import MediaRepository


class FakeMediaRepository(MediaRepository):
  def __init__(self):
    self.storage: MediaListResult = MediaListResult(
      items=[], total=0, page=1, page_size=10
    )

  async def create(self, media: Media) -> Media:
    media.id = uuid4()
    self.storage.items.append(media)
    self.storage.total += 1
    return media

  async def get(self, media_id: UUID) -> Optional[Media]:
    for media in self.storage.items:
      if media.id == media_id:
        return media

    return None

  async def list(
    self,
    page: int = 1,
    page_size: int = 10,
    filters: dict = {},
    sort_by: str = "created_at",
    sort_order: str = "desc",
  ) -> MediaListResult:
    start = (page - 1) * page_size
    end = start + page_size
    return MediaListResult(
      items=self.storage.items[start:end],
      total=len(self.storage.items),
      page=page,
      page_size=page_size,
    )

  async def update(self, media: Media) -> Media:
    for index, m in enumerate(self.storage.items):
      if m.id == media.id:
        self.storage.items[index] = media
        return media

    return None

  async def delete(self, media_ids: List[UUID]) -> bool:
    for media_id in media_ids:
      self.storage.items = [m for m in self.storage.items if m.id != media_id]
      self.storage.total -= 1

    return True
