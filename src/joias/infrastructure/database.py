"""
Configuração do banco de dados.

Este módulo contém a configuração e inicialização do banco de dados
usando SQLAlchemy.
"""
from functools import lru_cache
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .config import Settings, get_settings


class Database:
    """Classe para gerenciar a conexão com o banco de dados."""

    def __init__(self, settings: Settings):
        """
        Inicializa a conexão com o banco de dados.

        Args:
            settings: Configurações da aplicação
        """
        self._engine = create_engine(
            settings.DATABASE_URL,
            pool_size=settings.DATABASE_POOL_SIZE,
            max_overflow=settings.DATABASE_MAX_OVERFLOW,
        )
        self._session_factory = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine,
        )

    def get_session(self) -> Generator[Session, None, None]:
        """
        Retorna uma sessão do banco de dados.

        Yields:
            Session: Sessão do banco de dados
        """
        session = self._session_factory()
        try:
            yield session
        finally:
            session.close()


@lru_cache()
def get_database() -> Database:
    """
    Retorna uma instância do banco de dados.

    Esta função é decorada com @lru_cache para evitar
    que múltiplas instâncias sejam criadas.

    Returns:
        Database: Instância do banco de dados
    """
    return Database(get_settings()) 