"""
Configuração da sessão SQLAlchemy.

Este módulo configura e fornece a sessão do SQLAlchemy
para acesso ao banco de dados.
"""
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from ....settings import Settings

# Cria o engine do SQLAlchemy
engine = create_engine(Settings.DATABASE_URL, pool_pre_ping=True, echo=Settings.DEBUG)

# Cria a fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Retorna uma sessão do banco de dados.

    Esta função é usada como dependência do FastAPI para
    injetar sessões do banco de dados nos endpoints.

    Yields:
        Uma sessão do SQLAlchemy
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
