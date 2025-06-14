"""
Configurações da aplicação.

Este módulo centraliza todas as configurações da aplicação,
carregando-as de variáveis de ambiente.
"""
import os
from dataclasses import dataclass


@dataclass
class Settings:
    """
    Configurações da aplicação.

    Esta classe centraliza todas as configurações da aplicação,
    carregando-as de variáveis de ambiente com valores padrão.
    """

    # Ambiente
    DEBUG: bool = bool(int(os.getenv("DEBUG", "0")))

    # Banco de dados
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/joias"
    )

    # Segurança
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY", "insecure-dev-key-123"  # Não usar em produção!
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )
