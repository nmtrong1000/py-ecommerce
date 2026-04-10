import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4
from app.domain.entities.media_entity import Media
from app.infrastructure.persistence.repositories.media_repository_impl import (
  MediaRepositoryImpl,
)


@pytest.mark.asyncio
async def test_create_media(db_test_session: AsyncSession):
  repo = MediaRepositoryImpl(db_test_session)

  new_item = Media(
    id=uuid4(),
    url="http://example.com/image.png",
    media_type="image",
    mime_type="image/png",
    size=12345,
    created_at=None,
    updated_at=None,
  )

  retrieved_item = await repo.create(new_item)

  assert retrieved_item is not None
  assert retrieved_item.url == new_item.url


@pytest.mark.asyncio
async def test_get_media(db_test_session: AsyncSession):
  repo = MediaRepositoryImpl(db_test_session)

  new_item = Media(
    id=uuid4(),
    url="http://example.com/image.png",
    media_type="image",
    mime_type="image/png",
    size=12345,
    created_at=None,
    updated_at=None,
  )
  created = await repo.create(new_item)

  retrieved = await repo.get(created.id)

  assert retrieved is not None
  assert retrieved.id == created.id
  assert retrieved.url == created.url


@pytest.mark.asyncio
async def test_list_media(db_test_session: AsyncSession):
  repo = MediaRepositoryImpl(db_test_session)

  items = [
    Media(
      id=uuid4(),
      url=f"http://example.com/image_{i}.png",
      media_type="image",
      mime_type="image/png",
      size=12345 + i,
      created_at=None,
      updated_at=None,
    )
    for i in range(3)
  ]

  for item in items:
    await repo.create(item)

  results = await repo.list()

  assert results is not None
  assert len(results.items) >= 3


@pytest.mark.asyncio
async def test_update_media(db_test_session: AsyncSession):
  repo = MediaRepositoryImpl(db_test_session)

  new_item = Media(
    id=uuid4(),
    url="http://example.com/image.png",
    media_type="image",
    mime_type="image/png",
    size=12345,
    created_at=None,
    updated_at=None,
  )
  created = await repo.create(new_item)

  created.url = "http://example.com/updated.png"

  updated = await repo.update(created)

  assert updated is not None
  assert updated.url == "http://example.com/updated.png"

  retrieved = await repo.get(created.id)
  assert retrieved.url == "http://example.com/updated.png"


@pytest.mark.asyncio
async def test_delete_media(db_test_session: AsyncSession):
  repo = MediaRepositoryImpl(db_test_session)

  new_item = Media(
    id=uuid4(),
    url="http://example.com/image.png",
    media_type="image",
    mime_type="image/png",
    size=12345,
    created_at=None,
    updated_at=None,
  )
  created = await repo.create(new_item)

  await repo.delete([created.id])

  retrieved = await repo.get(created.id)
  assert retrieved is None
