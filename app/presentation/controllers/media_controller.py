from fastapi import APIRouter, Depends, Form
from typing import Annotated, List
from uuid import UUID
from app.application.dtos.media_dto import (
  MediaCreateDto,
  MediaUpdateDto,
  MediaResponseDto,
  MediaResponseListDto,
  MediaBulkDeleteDto,
)
from app.application.services.media_service import MediaService
from app.shared.api_response import ApiResponse, ResponseData
from app.infrastructure.di.media_di import get_media_service

router = APIRouter(tags=["Media"])


@router.post("/", response_model=ResponseData[MediaResponseDto])
async def create_media(
  data: Annotated[MediaCreateDto, Form()],
  service: MediaService = Depends(get_media_service),
):
  new_item = await service.create.execute(data)
  return ApiResponse.ok(data=MediaResponseDto(**new_item.__dict__))


@router.get("/", response_model=ResponseData[MediaResponseDto])
async def list_media(
  page: int = 1,
  page_size: int = 10,
  sort_by: str = "created_at",
  sort_order: str = "desc",
  service: MediaService = Depends(get_media_service),
):
  media_list = await service.list.execute(
    page=page, page_size=page_size, sort_by=sort_by, sort_order=sort_order, filters={}
  )
  return ApiResponse.ok(data=MediaResponseListDto(**media_list.__dict__))


@router.get("/{media_id}", response_model=ResponseData[MediaResponseDto])
async def get_media(media_id: UUID, service: MediaService = Depends(get_media_service)):
  item = await service.get.execute(media_id)

  if not item:
    return ApiResponse.not_found()

  return ApiResponse.ok(data=MediaResponseDto(**item.__dict__))


@router.put("/{media_id}", response_model=ResponseData[MediaResponseDto])
async def update_media(
  media_id: UUID,
  data: Annotated[MediaUpdateDto, Form()],
  service: MediaService = Depends(get_media_service),
):
  updated = await service.update.execute(media_id, data)
  return ApiResponse.ok(data=MediaResponseDto(**updated.__dict__))


@router.delete("/", response_model=ResponseData[MediaResponseDto])
async def bulk_delete_media(
  data: Annotated[MediaBulkDeleteDto, Form()],
  service: MediaService = Depends(get_media_service),
):
  deleted = await service.delete.execute(data.ids)
  return ApiResponse.ok(data=deleted)
