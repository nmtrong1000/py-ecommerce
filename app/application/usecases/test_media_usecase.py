import pytest
import pytest_asyncio
from app.application.usecases.media_usecase import (
  CreateMediaUseCase,
  UpdateMediaUseCase,
  ListMediaUseCase,
  GetMediaUseCase,
  DeleteMediaUseCase,
)
from app.application.dtos.media_dto import (
  MediaCreateDto,
  MediaUpdateDto,
)
from app.shared.mockup.fake_media_repository import FakeMediaRepository


@pytest_asyncio.fixture
async def repo() -> FakeMediaRepository:
  fake_repo = FakeMediaRepository()
  create_usecase = CreateMediaUseCase(fake_repo)
  for _ in range(15):
    dto = MediaCreateDto(
      url="https://example.com/image.png",
      media_type="image",
      mime_type="image/png",
      size=1024,
    )
    await create_usecase.execute(dto)
  return fake_repo


@pytest.mark.asyncio
async def test_create_media_should_create_successfully():
  fake_repo = FakeMediaRepository()
  usecase = CreateMediaUseCase(fake_repo)
  dto = MediaCreateDto(
    url="https://example.com/image.png",
    media_type="image",
    mime_type="image/png",
    size=1024,
  )

  result = await usecase.execute(dto)

  assert result is not None
  assert result.url == dto.url

  assert len(fake_repo.storage.items) == 1
  stored = fake_repo.storage.items[0]
  assert stored.url == dto.url


@pytest.mark.asyncio
async def test_get_media_should_be_empty(repo: FakeMediaRepository):
  usecase = GetMediaUseCase(repo)
  invalid_id = "test"

  result = await usecase.execute(invalid_id)
  assert result is None


@pytest.mark.asyncio
async def test_get_media_should_has_item(repo: FakeMediaRepository):
  get_usecase = GetMediaUseCase(repo)
  result = await get_usecase.execute(repo.storage.items[0].id)

  assert result is not None


@pytest.mark.asyncio
async def test_list_media_should_has_proper_pagination(repo: FakeMediaRepository):
  list_usecase = ListMediaUseCase(repo)
  result = await list_usecase.execute(
    page=2, page_size=5, filters={}, sort_by="created_at", sort_order="desc"
  )

  assert len(result.items) == 5


@pytest.mark.asyncio
async def test_update_media_should_update_successfully(repo: FakeMediaRepository):
  update_usecase = UpdateMediaUseCase(repo)
  update_item_id = repo.storage.items[0].id
  dto = MediaUpdateDto(mime_type="abc", size=2002)

  result = await update_usecase.execute(update_item_id, dto)

  assert result.size == dto.size
  assert result.mime_type == dto.mime_type


@pytest.mark.asyncio
async def test_delete_media_should_delete_successfully(repo: FakeMediaRepository):
  delete_usecase = DeleteMediaUseCase(repo)
  delete_item_id = repo.storage.items[0].id

  success = await delete_usecase.execute([delete_item_id])

  assert success
