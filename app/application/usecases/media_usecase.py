from datetime import datetime, timezone
from typing import Optional, List
from uuid import UUID, uuid4
from app.domain.entities.media_entity import Media, MediaListResult
from app.domain.repositories.media_repository import MediaRepository
from app.application.dtos.media_dto import (
  MediaCreateDto,
  MediaUpdateDto,
  MediaResponseDto,
  MediaResponseListDto,
)


def to_response_dto(item: Media) -> MediaResponseDto:
  return MediaResponseDto(
    id=item.id,
    url=item.url,
    media_type=item.media_type,
    mime_type=item.mime_type,
    size=item.size,
    created_at=item.created_at,
    updated_at=item.updated_at,
  )


def to_response_list_dto(resp: MediaListResult) -> MediaResponseListDto:
  return MediaResponseListDto(
    items=[to_response_dto(item) for item in resp.items],
    total=resp.total,
    page=resp.page,
    page_size=resp.page_size,
  )


class BaseMediaUseCase:
  def __init__(self, repo: MediaRepository):
    self.repo = repo


class CreateMediaUseCase(BaseMediaUseCase):
  async def execute(self, data: MediaCreateDto) -> MediaResponseDto:
    now = datetime.now(timezone.utc)
    result = await self.repo.create(
      Media(
        id=uuid4(),
        url=data.url,
        media_type=data.media_type,
        mime_type=data.mime_type,
        size=data.size,
        created_at=now,
        updated_at=now,
      )
    )

    return to_response_dto(result)


class GetMediaUseCase(BaseMediaUseCase):
  async def execute(self, item_id: UUID) -> Optional[MediaResponseDto]:
    result = await self.repo.get(item_id)
    if result is not None:
      return to_response_dto(result)

    return None


class ListMediaUseCase(BaseMediaUseCase):
  async def execute(
    self, page: int, page_size: int, filters: dict, sort_by: str, sort_order: str
  ) -> MediaResponseListDto:
    result = await self.repo.list(page, page_size, filters, sort_by, sort_order)
    return to_response_list_dto(result)


class UpdateMediaUseCase(BaseMediaUseCase):
  async def execute(
    self, item_id: UUID, data: MediaUpdateDto
  ) -> Optional[MediaResponseDto]:
    item = await self.repo.get(item_id)

    if not item:
      raise ValueError(f"Media with id {item_id} not found")

    udpated_data = data.model_dump(exclude_unset=True)
    for field, value in udpated_data.items():
      if field == "url":
        value = str(value)

      setattr(item, field, value)

    result = await self.repo.update(item)
    return to_response_dto(result)


class DeleteMediaUseCase(BaseMediaUseCase):
  async def execute(self, data: List[UUID]) -> bool:
    success = True

    if isinstance(data, list):
      success = await self.repo.delete(data)
    else:
      success = await self.repo.delete([data])

    return success
