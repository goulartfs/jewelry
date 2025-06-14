"""
Configuração do pytest.
"""
import os
from datetime import datetime
from typing import Generator
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.joias.application.identity.auth_service import AuthService
from src.joias.application.identity.permissao_service import PermissaoService
from src.joias.application.identity.usuario_service import UsuarioService
from src.joias.infrastructure.config.settings import Settings, get_settings
from src.joias.infrastructure.persistence.sqlalchemy.base import Base
from src.joias.infrastructure.persistence.sqlalchemy.models.permissao import PermissaoModel
from src.joias.infrastructure.persistence.sqlalchemy.models.usuario import UsuarioModel
from src.joias.infrastructure.persistence.sqlalchemy.repositories.permissao_repository import (
    SQLPermissaoRepository,
)
from src.joias.infrastructure.persistence.sqlalchemy.repositories.usuario_repository import (
    SQLUsuarioRepository,
)
from src.joias.infrastructure.persistence.sqlalchemy.session import get_db_session
from src.joias.presentation.api.app import app


def get_test_settings() -> Settings:
    """
    Retorna as configurações de teste.

    Returns:
        Configurações de teste
    """
    return Settings(
        database_url="sqlite:///./test.db",
        secret_key="test-secret-key",
        token_expiration=24,
    )


@pytest.fixture(scope="session")
def engine():
    """
    Fixture que retorna uma instância do engine do SQLAlchemy.
    """
    return create_engine(
        get_test_settings().database_url,
        connect_args={"check_same_thread": False},
    )


@pytest.fixture(scope="session")
def tables(engine):
    """
    Fixture que cria as tabelas no banco de dados.
    """
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def session(engine, tables) -> Generator[Session, None, None]:
    """
    Fixture que retorna uma sessão do SQLAlchemy.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def usuario_repository(session) -> SQLUsuarioRepository:
    """
    Fixture que retorna uma instância do repositório de usuários.
    """
    return SQLUsuarioRepository(session)


@pytest.fixture
def permissao_repository(session) -> SQLPermissaoRepository:
    """
    Fixture que retorna uma instância do repositório de permissões.
    """
    return SQLPermissaoRepository(session)


@pytest.fixture
def auth_service(usuario_repository) -> AuthService:
    """
    Fixture que retorna uma instância do serviço de autenticação.
    """
    settings = get_test_settings()
    return AuthService(
        usuario_repository=usuario_repository,
        secret_key=settings.secret_key,
        token_expiration=settings.token_expiration,
    )


@pytest.fixture
def usuario_service(usuario_repository, auth_service) -> UsuarioService:
    """
    Fixture que retorna uma instância do serviço de usuário.
    """
    return UsuarioService(
        usuario_repository=usuario_repository,
        auth_service=auth_service,
    )


@pytest.fixture
def permissao_service(permissao_repository) -> PermissaoService:
    """
    Fixture que retorna uma instância do serviço de permissão.
    """
    return PermissaoService(permissao_repository)


@pytest.fixture
def usuario_model(session: Session, auth_service: AuthService) -> UsuarioModel:
    """
    Fixture que cria um usuário no banco de dados.
    """
    senha_hash = auth_service.gerar_hash_senha("senha123")
    usuario = UsuarioModel(
        id=uuid4(),
        nome="John Doe",
        email="john@doe.com",
        senha_hash=senha_hash,
        ativo=True,
        data_criacao=datetime.utcnow(),
    )
    session.add(usuario)
    session.commit()
    return usuario


@pytest.fixture
def permissao_model(session: Session) -> PermissaoModel:
    """
    Fixture que cria uma permissão no banco de dados.
    """
    permissao = PermissaoModel(
        id=uuid4(),
        nome="ADMIN",
        descricao="Administrador do sistema",
        data_criacao=datetime.utcnow(),
    )
    session.add(permissao)
    session.commit()
    return permissao


@pytest.fixture
def token(usuario_model, auth_service) -> str:
    """
    Fixture que retorna um token de autenticação.
    """
    return auth_service.autenticar(
        email=usuario_model.email,
        senha="senha123",
    )


@pytest.fixture
def client(session) -> Generator[TestClient, None, None]:
    """
    Fixture que retorna um cliente de teste do FastAPI.
    """

    def override_get_db_session():
        try:
            yield session
        finally:
            pass

    def override_get_settings():
        return get_test_settings()

    app.dependency_overrides[get_db_session] = override_get_db_session
    app.dependency_overrides[get_settings] = override_get_settings

    yield TestClient(app)

    app.dependency_overrides.clear() 