from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class _Settings(BaseSettings):
    application_es_collection: str | None = None
    application_vector_es_collection: str | None = None
    open_api_key: str | None = None

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings() -> _Settings:
    return _Settings()
