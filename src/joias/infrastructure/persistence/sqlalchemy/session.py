"""
Configuração da sessão do SQLAlchemy.
"""
from typing import Generator

from sqlalchemy.orm import Session

from .base import SessionLocal


def get_db_session() -> Generator[Session, None, None]:
    """
    Retorna uma sessão do SQLAlchemy.

    Yields:
        Sessão do SQLAlchemy
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
