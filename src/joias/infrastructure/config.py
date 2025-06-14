"""
Configurações da aplicação.

Este módulo define as configurações da aplicação usando
o Pydantic para validação.
"""
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configurações da aplicação."""

    # Configurações do banco de dados
    database_url: str = "postgresql://postgres:postgres@localhost:5432/joias"

    # Configurações do JWT
    jwt_secret_key: str = "secret"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 30

    # Configurações do servidor
    host: str = "localhost"
    port: int = 8000
    debug: bool = False
    reload: bool = False

    # Configurações do CORS
    cors_origins: list[str] = ["*"]
    cors_methods: list[str] = ["*"]
    cors_headers: list[str] = ["*"]

    # Configurações do Swagger
    title: str = "API de Joias"
    description: str = "API para gerenciamento de joias"
    version: str = "0.1.0"
    openapi_url: Optional[str] = "/openapi.json"
    docs_url: Optional[str] = "/docs"
    redoc_url: Optional[str] = "/redoc"

    class Config:
        """Configurações do Pydantic."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Retorna as configurações da aplicação.
    
    Returns:
        Configurações da aplicação
    """
    return Settings() 