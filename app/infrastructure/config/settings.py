from pydantic import ConfigDict
from pydantic_settings import BaseSettings


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
  DEBUG: bool


settings = Settings()
