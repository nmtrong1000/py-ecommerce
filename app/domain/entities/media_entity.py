from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from typing import List


@dataclass
class Media:
  id: UUID
  url: str
  media_type: str
  mime_type: str
  size: int
  created_at: datetime
  updated_at: datetime


@dataclass
class MediaListResult:
  items: List[Media]
  total: int
  page: int
  page_size: int
