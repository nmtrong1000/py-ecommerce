from typing import Optional, Dict, List
from uuid import UUID
from app.shared.caching import build_get_key, build_list_key
from app.domain.entities.media_entity import Media, MediaListResult
from app.domain.repositories.media_repository import MediaRepository
from app.domain.repositories.cache_repository import CacheRepository
from app.infrastructure.persistence.mappers.media_mapper import MediaMapper


class MediaRepositoryFacade:
  def __init__(self, db_repo: MediaRepository, cache_repo: CacheRepository):
    self.db_repo = db_repo
    self.cache_repo = cache_repo

  async def create(self, media: Media) -> Media:
    result = await self.db_repo.create(media)

    if self.cache_repo is not None:
      await self.cache_repo.delete_pattern("media:list:*")

    return result

  async def get(self, media_id: UUID) -> Optional[Media]:
    cache_key = build_get_key("media", media_id)
    if self.cache_repo is not None:
      cached_data = await self.cache_repo.get(cache_key)

      if cached_data:
        return MediaMapper.from_json(cached_data)

    result = await self.db_repo.get(media_id)

    if result and self.cache_repo is not None:
      await self.cache_repo.set(
        key=cache_key, value=MediaMapper.to_json(result), ttl=3600
      )

    return result

  async def list(
    self,
    page: int = 1,
    page_size: int = 10,
    filters: Optional[Dict] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
  ) -> MediaListResult:
    cache_key = build_list_key("media", page, page_size, filters, sort_by, sort_order)
    if self.cache_repo is not None:
      cached_data = await self.cache_repo.get(cache_key)

      if cached_data:
        return MediaMapper.from_list_json(cached_data)

    result = await self.db_repo.list(
      page=page,
      page_size=page_size,
      filters=filters,
      sort_by=sort_by,
      sort_order=sort_order,
    )

    if len(result.items) > 0 and self.cache_repo is not None:
      await self.cache_repo.set(
        key=cache_key, value=MediaMapper.to_list_json(result), ttl=3600
      )

    return result

  async def update(self, media: Media) -> Media:
    result = await self.db_repo.update(media)

    if self.cache_repo is not None:
      cache_key = build_get_key("media", str(media.id))
      await self.cache_repo.delete(cache_key)
      await self.cache_repo.delete_pattern("media:list:*")

    return result

  async def delete(self, media_ids: List[UUID]) -> bool:
    result = await self.db_repo.update(media_ids)

    if result and self.db_repo is not None:
      for item_id in media_ids:
        get_cache_key = build_get_key("media", str(item_id))
        await self.cache_repo.delete(get_cache_key)

      await self.cache_repo.delete_pattern("media:list:*")

    return result
