import os

os.environ["DB_HOST"] = "localhost"

import logging
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from app.infrastructure.persistence.base import DATABASE_URL
from httpx import AsyncClient, ASGITransport
from app.infrastructure.persistence.base import get_db_session
from app.main import app

logger = logging.getLogger(__name__)

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncTestingSessionLocal = sessionmaker(
  bind=engine,
  class_=AsyncSession,
  expire_on_commit=False,
)


@pytest_asyncio.fixture(scope="function")
async def db_test_session() -> AsyncGenerator[AsyncSession, None]:
  async with engine.connect() as connection:
    logger.info("DB connected")
    transaction = await connection.begin()
    async_session = AsyncTestingSessionLocal(bind=connection)

    try:
      yield async_session
      await async_session.flush()
    finally:
      await async_session.close()
      await transaction.rollback()

  await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def client(db_test_session: AsyncSession):
  def _get_test_db():
    yield db_test_session

  app.dependency_overrides[get_db_session] = _get_test_db
  async with AsyncClient(
    transport=ASGITransport(app=app),
    base_url="http://testserver",
  ) as ac:
    yield ac
  app.dependency_overrides.clear()
