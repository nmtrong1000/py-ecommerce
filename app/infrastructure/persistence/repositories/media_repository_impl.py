from typing import List, Optional, Dict
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy import func, asc, desc
from app.domain.entities.media_entity import Media, MediaListResult
from app.domain.repositories.media_repository import MediaRepository
from app.infrastructure.persistence.models.media_model import MediaModel
from app.infrastructure.persistence.mappers.media_mapper import MediaMapper


class MediaRepositoryImpl(MediaRepository):
  def __init__(self, session: AsyncSession):
    self.session = session

  async def create(self, media: Media) -> Media:
    media_model = MediaMapper.to_model(media)
    self.session.add(media_model)
    await self.session.flush()
    await self.session.refresh(media_model)
    return MediaMapper.to_entity(media_model)

  async def get(self, media_id: UUID) -> Optional[Media]:
    result = await self.session.execute(
      select(MediaModel).where(MediaModel.id == media_id)
    )
    media_model = result.scalar_one_or_none()
    return MediaMapper.to_entity(media_model)

  async def list(
    self,
    page: int = 1,
    page_size: int = 10,
    filters: Optional[Dict] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
  ) -> MediaListResult:
    query = select(MediaModel)

    # apply filters
    if filters:
      for field, value in filters.items():
        column = getattr(MediaModel, field, None)
        if column is not None:
          query = query.where(column == value)

    # apply sorting
    column = getattr(MediaModel, sort_by, MediaModel.created_at)
    if sort_order.lower() == "desc":
      query = query.order_by(desc(column))
    else:
      query = query.order_by(asc(column))

    # count total
    total_result = await self.session.execute(
      select(func.count()).select_from(query.subquery())
    )
    total = total_result.scalar_one()

    # apply pagination
    query = query.offset((page - 1) * page_size).limit(page_size)

    # execute
    result = await self.session.execute(query)
    media_models = result.scalars().all()

    items = [MediaMapper.to_entity(m) for m in media_models]

    return MediaListResult(items=items, total=total, page=page, page_size=page_size)

  async def update(self, media: Media) -> Media:
    result = await self.session.execute(
      select(MediaModel).where(MediaModel.id == media.id)
    )

    media_model = result.scalar_one()
    MediaMapper.update_model(media_model, media)
    await self.session.flush()
    await self.session.refresh(media_model)
    return MediaMapper.to_entity(media_model)

  async def delete(self, media_ids: List[UUID]) -> bool:
    query = select(MediaModel).where(MediaModel.id.in_(media_ids))
    result = await self.session.execute(query)
    media_models = result.scalars().all()

    if not media_models or len(media_models) == 0:
      return False

    for media_model in media_models:
      await self.session.delete(media_model)

    await self.session.flush()

    return True
