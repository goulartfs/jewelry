"""
Configurações da aplicação.
"""
import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configurações da aplicação.
    """

    database_url: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./joias.db",
    )
    secret_key: str = os.getenv(
        "SECRET_KEY",
        "your-secret-key",
    )
    token_expiration: int = int(
        os.getenv(
            "TOKEN_EXPIRATION",
            "24",
        )
    )


@lru_cache
def get_settings() -> Settings:
    """
    Retorna as configurações da aplicação.

    Returns:
        Configurações da aplicação
    """
    return Settings() 