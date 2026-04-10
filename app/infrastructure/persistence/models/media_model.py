from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from uuid import uuid4
from app.infrastructure.persistence.base import Base


class MediaModel(Base):
  __tablename__ = "media"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
  url = Column(String, nullable=False)
  media_type = Column(String, nullable=False)
  mime_type = Column(String, nullable=False)
  size = Column(Integer, nullable=False)
  created_at = Column(DateTime(timezone=True), server_default=func.now())
  updated_at = Column(
    DateTime(timezone=True), onupdate=func.now(), server_default=func.now()
  )
