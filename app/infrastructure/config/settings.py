import logging
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

logging.basicConfig(
  level=logging.DEBUG,  # <-- THIS enables debug logs
  format="%(levelname)s:    %(message)s",
)


class Settings(BaseSettings):
  model_config = ConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    extra="allow",
  )
  DB_HOST: str
  DB_PORT: str
  DB_NAME: str
  DB_USER: str
  DB_PWD: str
  REDIS_HOST: str
  REDIS_PORT: str
  REDIS_DB: str
  REDIS_PASSWORD: str
  DEBUG: bool


settings = Settings()
