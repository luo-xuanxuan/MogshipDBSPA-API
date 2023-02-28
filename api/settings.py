from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_NAME: str = "mogship"
    DB_USER: str = "mogship"
    DB_PASSWORD: str = "mogship"
    DB_PORT: int = 3306
    CORS_ORIGIN: str = "http://localhost:5173"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
