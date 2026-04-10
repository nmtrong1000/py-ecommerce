from pydantic import BaseModel, HttpUrl, Field, ConfigDict
from enum import Enum
from typing import Optional, List
from uuid import UUID
from datetime import datetime


class MediaType(str, Enum):
  IMAGE = "image"
  VIDEO = "video"
  DOCUMENT = "document"


form_data_examples = {
  "examples": [
    {
      "url": "https://images.unsplash.com/photo-1773332611516-93826171cef2?q=80&w=987&auto=format&fit=crop",
      "media_type": "image",
      "mime_type": "image/png",
      "size": 2048,
    }
  ]
}


class MediaCreateDto(BaseModel):
  url: HttpUrl
  media_type: MediaType
  mime_type: str = Field(..., pattern=r"^[a-z]+/[a-z0-9\-\.+]+$")
  size: int = Field(..., gt=0)

  model_config = ConfigDict(json_schema_extra=form_data_examples, extra="forbid")


class MediaUpdateDto(BaseModel):
  url: Optional[HttpUrl] = None
  media_type: Optional[MediaType] = None
  mime_type: Optional[str] = None
  size: Optional[int] = Field(None, gt=0)

  model_config = ConfigDict(json_schema_extra=form_data_examples, extra="forbid")


class MediaBulkDeleteDto(BaseModel):
  ids: List[UUID]


class MediaResponseDto(BaseModel):
  id: UUID
  url: Optional[HttpUrl] = None
  media_type: Optional[MediaType] = None
  mime_type: Optional[str] = None
  size: Optional[int] = Field(None, gt=0)
  created_at: datetime
  updated_at: datetime

  model_config = ConfigDict(from_attributes=True)


class MediaResponseListDto(BaseModel):
  items: List[MediaResponseDto] = []
  total: int
  page: int
  page_size: int

  model_config = ConfigDict(from_attributes=True)
