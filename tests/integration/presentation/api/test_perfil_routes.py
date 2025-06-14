"""
Testes de integração para os endpoints de perfil.

Este módulo contém os testes de integração para os
endpoints relacionados a perfis.
"""
import uuid
from datetime import datetime

import pytest
from fastapi import status
from sqlalchemy.orm import Session

from src.joias.infrastructure.persistence.sqlalchemy.models import (
    Perfil as PerfilModel,
    Usuario as UsuarioModel,
)


@pytest.fixture
def perfil(session: Session):
    """Fixture que cria um perfil no banco de dados."""
    perfil = PerfilModel(
        id=uuid.uuid4(),
        nome="Administrador",
        descricao="Perfil de administrador",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    session.add(perfil)
    session.commit()
    return perfil


@pytest.fixture
def usuario(session: Session):
    """Fixture que cria um usuário no banco de dados."""
    usuario = UsuarioModel(
        id=uuid.uuid4(),
        nome="John Doe",
        email="john@example.com",
        senha_hashed="hash123",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    session.add(usuario)
    session.commit()
    return usuario


def test_criar_perfil_sucesso(client, session: Session):
    """Deve criar um perfil com sucesso."""
    # Arrange
    dados = {
        "nome": "Administrador",
        "descricao": "Perfil de administrador"
    }

    # Act
    response = client.post("/api/perfis", json=dados)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    dados_resposta = response.json()
    assert dados_resposta["nome"] == "Administrador"
    assert dados_resposta["descricao"] == "Perfil de administrador"
    assert "id" in dados_resposta
    assert "created_at" in dados_resposta
    assert "updated_at" in dados_resposta

    # Verificar no banco
    perfil = session.query(PerfilModel).filter(
        PerfilModel.nome == "Administrador"
    ).first()
    assert perfil is not None
    assert str(perfil.id) == dados_resposta["id"]


def test_criar_perfil_nome_duplicado(client, perfil):
    """Deve falhar ao criar perfil com nome duplicado."""
    # Arrange
    dados = {
        "nome": perfil.nome,
        "descricao": "Nova descrição"
    }

    # Act
    response = client.post("/api/perfis", json=dados)

    # Assert
    assert response.status_code == status.HTTP_409_CONFLICT
    assert "erro" in response.json()
    assert f"Já existe um perfil com o nome '{perfil.nome}'" in response.json()["erro"]


def test_criar_perfil_dados_invalidos(client):
    """Deve falhar ao criar perfil com dados inválidos."""
    # Arrange
    dados = {
        "nome": "",  # nome vazio
        "descricao": "Descrição"
    }

    # Act
    response = client.post("/api/perfis", json=dados)

    # Assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_associar_usuario_sucesso(client, perfil, usuario, session: Session):
    """Deve associar um usuário a um perfil com sucesso."""
    # Act
    response = client.put(f"/api/perfis/{perfil.id}/usuarios/{usuario.id}")

    # Assert
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verificar no banco
    usuario_db = session.query(UsuarioModel).filter(
        UsuarioModel.id == usuario.id
    ).first()
    assert usuario_db is not None
    assert len(usuario_db.perfis) == 1
    assert usuario_db.perfis[0].id == perfil.id


def test_associar_usuario_perfil_nao_encontrado(client, usuario):
    """Deve falhar ao associar usuário a perfil inexistente."""
    # Arrange
    perfil_id = uuid.uuid4()

    # Act
    response = client.put(f"/api/perfis/{perfil_id}/usuarios/{usuario.id}")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "erro" in response.json()
    assert f"Perfil com ID '{perfil_id}' não encontrado" in response.json()["erro"]


def test_associar_usuario_nao_encontrado(client, perfil):
    """Deve falhar ao associar usuário inexistente a perfil."""
    # Arrange
    usuario_id = uuid.uuid4()

    # Act
    response = client.put(f"/api/perfis/{perfil.id}/usuarios/{usuario_id}")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "erro" in response.json()
    assert f"Usuário com ID '{usuario_id}' não encontrado" in response.json()["erro"] 