"""
Configuração da sessão do SQLAlchemy.

Este módulo configura a conexão com o banco de dados e
fornece funções para gerenciar sessões do SQLAlchemy.
"""
import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Obtém a URL do banco de dados das variáveis de ambiente
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/joias"
)

# Cria o engine do SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verifica conexão antes de usar
    pool_size=5,         # Tamanho do pool de conexões
    max_overflow=10      # Máximo de conexões extras
)

# Cria a fábrica de sessões
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db() -> Generator[Session, None, None]:
    """
    Retorna uma sessão do banco de dados.

    Esta função é usada como dependência no FastAPI para
    injetar sessões do banco de dados nos endpoints.

    Yields:
        Session: Sessão do banco de dados
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 