from app.application.usecases.media_usecase import (
  CreateMediaUseCase,
  ListMediaUseCase,
  GetMediaUseCase,
  UpdateMediaUseCase,
  DeleteMediaUseCase,
)
from app.domain.repositories.media_repository import MediaRepository


class MediaService:
  def __init__(self, repo: MediaRepository):
    self.create = CreateMediaUseCase(repo)
    self.list = ListMediaUseCase(repo)
    self.get = GetMediaUseCase(repo)
    self.update = UpdateMediaUseCase(repo)
    self.delete = DeleteMediaUseCase(repo)
