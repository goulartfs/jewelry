"""
Gerenciamento de sessões do SQLAlchemy.

Este módulo define as funções para gerenciar as sessões
do SQLAlchemy.
"""
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.joias.infrastructure.config import get_settings


def get_engine():
    """
    Cria e retorna o engine do SQLAlchemy.
    
    Returns:
        Engine do SQLAlchemy
    """
    settings = get_settings()
    return create_engine(settings.database_url)


def get_session() -> Generator[Session, None, None]:
    """
    Cria e retorna uma sessão do SQLAlchemy.
    
    Yields:
        Sessão do SQLAlchemy
    """
    engine = get_engine()
    session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = session_factory()
    try:
        yield session
    finally:
        session.close()
