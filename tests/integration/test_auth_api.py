"""
Testes de integração para a API de autenticação.
"""
from datetime import datetime
from uuid import uuid4

import pytest
from fastapi import status
from sqlalchemy.orm import Session

from src.joias.application.identity.auth_service import AuthService
from src.joias.domain.shared.value_objects import Email
from src.joias.infrastructure.persistence.sqlalchemy.models.usuario import UsuarioModel
from src.joias.infrastructure.persistence.sqlalchemy.repositories.usuario_repository import (
    SQLUsuarioRepository,
)


@pytest.fixture
def auth_service(session: Session):
    """
    Fixture que retorna uma instância do serviço de autenticação.
    """
    return AuthService(
        usuario_repository=SQLUsuarioRepository(session),
        secret_key="test-secret-key",
        token_expiration=24,
    )


@pytest.fixture
def usuario_model(session: Session, auth_service: AuthService):
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


def test_login_com_sucesso(client, usuario_model):
    """
    Testa o login com sucesso.
    """
    # Arrange
    dados = {
        "username": usuario_model.email,
        "password": "senha123",
    }

    # Act
    response = client.post("/auth/login", data=dados)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_com_credenciais_invalidas(client, usuario_model):
    """
    Testa o login com credenciais inválidas.
    """
    # Arrange
    dados = {
        "username": usuario_model.email,
        "password": "senha_errada",
    }

    # Act
    response = client.post("/auth/login", data=dados)

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "credenciais inválidas" in response.json()["detail"].lower()


def test_login_com_usuario_inativo(client, usuario_model, session):
    """
    Testa o login com usuário inativo.
    """
    # Arrange
    usuario_model.ativo = False
    session.commit()

    dados = {
        "username": usuario_model.email,
        "password": "senha123",
    }

    # Act
    response = client.post("/auth/login", data=dados)

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "inativo" in response.json()["detail"].lower()


def test_me_com_sucesso(client, usuario_model, auth_service):
    """
    Testa a rota /me com sucesso.
    """
    # Arrange
    token = auth_service.autenticar(
        email=usuario_model.email,
        senha="senha123",
    )

    # Act
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == str(usuario_model.id)
    assert response.json()["nome"] == usuario_model.nome
    assert response.json()["email"] == usuario_model.email
    assert response.json()["ativo"] == usuario_model.ativo


def test_me_sem_token(client):
    """
    Testa a rota /me sem token.
    """
    # Act
    response = client.get("/auth/me")

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "não autenticado" in response.json()["detail"].lower()


def test_me_com_token_invalido(client):
    """
    Testa a rota /me com token inválido.
    """
    # Act
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer token_invalido"},
    )

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "token inválido" in response.json()["detail"].lower()


def test_me_com_usuario_inativo(client, usuario_model, auth_service, session):
    """
    Testa a rota /me com usuário inativo.
    """
    # Arrange
    token = auth_service.autenticar(
        email=usuario_model.email,
        senha="senha123",
    )

    usuario_model.ativo = False
    session.commit()

    # Act
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "inativo" in response.json()["detail"].lower() 