from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.persistence.base import get_db_session
from app.infrastructure.di.cache_di import get_cache_repository
from app.infrastructure.persistence.repositories.media_repository_impl import (
  MediaRepositoryImpl,
)
from app.infrastructure.persistence.repositories.media_repository_facade import (
  MediaRepositoryFacade,
)
from app.domain.repositories.cache_repository import CacheRepository
from app.application.services.media_service import MediaService


def get_media_repo(
  db: AsyncSession = Depends(get_db_session),
  cache_repo: CacheRepository = Depends(get_cache_repository),
) -> MediaRepositoryFacade:
  return MediaRepositoryFacade(
    db_repo=MediaRepositoryImpl(session=db), cache_repo=cache_repo
  )


def get_media_service(
  repo: MediaRepositoryFacade = Depends(get_media_repo),
) -> MediaService:
  return MediaService(repo=repo)
