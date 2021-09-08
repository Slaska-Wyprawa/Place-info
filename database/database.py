from functools import lru_cache

from sqlmodel import create_engine

from config.config import Settings


@lru_cache()
def get_settings():
    return Settings()


settings: Settings = get_settings()
database_connection_url = settings.database_connection_url

engine = create_engine(database_connection_url, echo=True)
