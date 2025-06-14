"""
Configuração do pytest.

Este módulo configura o ambiente de testes, fornecendo
fixtures e configurações compartilhadas.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.joias.infrastructure.persistence.sqlalchemy.base import Base


@pytest.fixture(scope="session")
def engine():
    """Fixture que fornece o engine do SQLAlchemy."""
    return create_engine("sqlite:///:memory:")


@pytest.fixture(scope="session")
def tables(engine):
    """Fixture que cria as tabelas no banco de testes."""
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(engine, tables):
    """
    Fixture que fornece uma sessão do SQLAlchemy.

    Esta fixture cria uma nova transação para cada teste
    e faz rollback no final, garantindo o isolamento.
    """
    connection = engine.connect()
    transaction = connection.begin()

    DBSession = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = DBSession()

    yield session

    session.close()
    transaction.rollback()
    connection.close()
