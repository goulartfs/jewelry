"""
Testes de integração para a API de usuário.
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


@pytest.fixture
def token(usuario_model, auth_service):
    """
    Fixture que retorna um token de autenticação.
    """
    return auth_service.autenticar(
        email=usuario_model.email,
        senha="senha123",
    )


def test_criar_usuario_com_sucesso(client):
    """
    Testa a criação de um usuário com sucesso.
    """
    # Arrange
    dados = {
        "nome": "Jane Doe",
        "email": "jane@doe.com",
        "senha": "senha123",
    }

    # Act
    response = client.post("/usuarios", json=dados)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["nome"] == dados["nome"]
    assert response.json()["email"] == dados["email"]
    assert response.json()["ativo"] is True
    assert "id" in response.json()
    assert "data_criacao" in response.json()


def test_criar_usuario_com_email_invalido(client):
    """
    Testa a criação de um usuário com email inválido.
    """
    # Arrange
    dados = {
        "nome": "Jane Doe",
        "email": "email_invalido",
        "senha": "senha123",
    }

    # Act
    response = client.post("/usuarios", json=dados)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email inválido" in response.json()["detail"].lower()


def test_criar_usuario_com_email_ja_existente(client, usuario_model):
    """
    Testa a criação de um usuário com email já existente.
    """
    # Arrange
    dados = {
        "nome": "Jane Doe",
        "email": usuario_model.email,
        "senha": "senha123",
    }

    # Act
    response = client.post("/usuarios", json=dados)

    # Assert
    assert response.status_code == status.HTTP_409_CONFLICT
    assert "já existe" in response.json()["detail"].lower()


def test_buscar_usuario_por_id_com_sucesso(client, usuario_model, token):
    """
    Testa a busca de um usuário por ID com sucesso.
    """
    # Act
    response = client.get(
        f"/usuarios/{usuario_model.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == str(usuario_model.id)
    assert response.json()["nome"] == usuario_model.nome
    assert response.json()["email"] == usuario_model.email
    assert response.json()["ativo"] == usuario_model.ativo


def test_buscar_usuario_por_id_nao_encontrado(client, token):
    """
    Testa a busca de um usuário por ID não encontrado.
    """
    # Act
    response = client.get(
        f"/usuarios/{uuid4()}",
        headers={"Authorization": f"Bearer {token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "não encontrado" in response.json()["detail"].lower()


def test_buscar_usuario_por_id_sem_autenticacao(client, usuario_model):
    """
    Testa a busca de um usuário por ID sem autenticação.
    """
    # Act
    response = client.get(f"/usuarios/{usuario_model.id}")

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "não autenticado" in response.json()["detail"].lower()


def test_listar_usuarios_com_sucesso(client, usuario_model, token):
    """
    Testa a listagem de usuários com sucesso.
    """
    # Act
    response = client.get(
        "/usuarios",
        headers={"Authorization": f"Bearer {token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == str(usuario_model.id)
    assert response.json()[0]["nome"] == usuario_model.nome
    assert response.json()[0]["email"] == usuario_model.email
    assert response.json()[0]["ativo"] == usuario_model.ativo


def test_listar_usuarios_sem_autenticacao(client):
    """
    Testa a listagem de usuários sem autenticação.
    """
    # Act
    response = client.get("/usuarios")

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "não autenticado" in response.json()["detail"].lower()


def test_atualizar_usuario_com_sucesso(client, usuario_model, token):
    """
    Testa a atualização de um usuário com sucesso.
    """
    # Arrange
    dados = {
        "nome": "Jane Doe",
        "email": "jane@doe.com",
        "senha": "senha456",
        "ativo": False,
    }

    # Act
    response = client.put(
        f"/usuarios/{usuario_model.id}",
        json=dados,
        headers={"Authorization": f"Bearer {token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == str(usuario_model.id)
    assert response.json()["nome"] == dados["nome"]
    assert response.json()["email"] == dados["email"]
    assert response.json()["ativo"] == dados["ativo"]


def test_atualizar_usuario_nao_encontrado(client, token):
    """
    Testa a atualização de um usuário não encontrado.
    """
    # Arrange
    dados = {
        "nome": "Jane Doe",
    }

    # Act
    response = client.put(
        f"/usuarios/{uuid4()}",
        json=dados,
        headers={"Authorization": f"Bearer {token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "não encontrado" in response.json()["detail"].lower()


def test_atualizar_usuario_com_email_ja_existente(
    client,
    usuario_model,
    token,
    session,
):
    """
    Testa a atualização de um usuário com email já existente.
    """
    # Arrange
    outro_usuario = UsuarioModel(
        id=uuid4(),
        nome="Jane Doe",
        email="jane@doe.com",
        senha_hash="hash123",
        ativo=True,
        data_criacao=datetime.utcnow(),
    )
    session.add(outro_usuario)
    session.commit()

    dados = {
        "email": outro_usuario.email,
    }

    # Act
    response = client.put(
        f"/usuarios/{usuario_model.id}",
        json=dados,
        headers={"Authorization": f"Bearer {token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_409_CONFLICT
    assert "já existe" in response.json()["detail"].lower()


def test_atualizar_usuario_sem_autenticacao(client, usuario_model):
    """
    Testa a atualização de um usuário sem autenticação.
    """
    # Arrange
    dados = {
        "nome": "Jane Doe",
    }

    # Act
    response = client.put(
        f"/usuarios/{usuario_model.id}",
        json=dados,
    )

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "não autenticado" in response.json()["detail"].lower()


def test_excluir_usuario_com_sucesso(client, usuario_model, token):
    """
    Testa a exclusão de um usuário com sucesso.
    """
    # Act
    response = client.delete(
        f"/usuarios/{usuario_model.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_excluir_usuario_nao_encontrado(client, token):
    """
    Testa a exclusão de um usuário não encontrado.
    """
    # Act
    response = client.delete(
        f"/usuarios/{uuid4()}",
        headers={"Authorization": f"Bearer {token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "não encontrado" in response.json()["detail"].lower()


def test_excluir_usuario_sem_autenticacao(client, usuario_model):
    """
    Testa a exclusão de um usuário sem autenticação.
    """
    # Act
    response = client.delete(f"/usuarios/{usuario_model.id}")

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "não autenticado" in response.json()["detail"].lower() 