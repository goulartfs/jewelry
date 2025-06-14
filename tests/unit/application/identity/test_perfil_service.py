"""
Testes unitários para o serviço de perfil.

Este módulo contém os testes unitários para o serviço
de perfil.
"""
import uuid
from datetime import datetime
from unittest.mock import Mock

import pytest

from src.joias.application.identity.perfil_service import (
    PerfilService,
    CriarPerfilDTO,
    PerfilDTO,
)
from src.joias.domain.entities.autorizacao import Perfil
from src.joias.infrastructure.persistence.sqlalchemy.models import (
    Perfil as PerfilModel,
    Usuario as UsuarioModel,
)


@pytest.fixture
def repository():
    """Fixture que cria um mock do repositório."""
    return Mock()


@pytest.fixture
def service(repository):
    """Fixture que cria o serviço de perfil."""
    return PerfilService(repository)


@pytest.fixture
def perfil_model():
    """Fixture que cria um modelo de perfil."""
    return PerfilModel(
        id=uuid.uuid4(),
        nome="Administrador",
        descricao="Perfil de administrador",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


def test_criar_perfil_sucesso(service, repository, perfil_model):
    """Deve criar um perfil com sucesso."""
    # Arrange
    repository.buscar_por_nome.return_value = None
    repository.criar.return_value = perfil_model
    dto = CriarPerfilDTO(
        nome="Administrador",
        descricao="Perfil de administrador"
    )

    # Act
    resultado = service.criar_perfil(dto)

    # Assert
    assert isinstance(resultado, PerfilDTO)
    assert resultado.nome == "Administrador"
    assert resultado.descricao == "Perfil de administrador"
    repository.buscar_por_nome.assert_called_once_with("Administrador")
    repository.criar.assert_called_once()


def test_criar_perfil_nome_duplicado(service, repository):
    """Deve falhar ao criar perfil com nome duplicado."""
    # Arrange
    repository.buscar_por_nome.return_value = PerfilModel()
    dto = CriarPerfilDTO(nome="Administrador")

    # Act/Assert
    with pytest.raises(ValueError, match="Já existe um perfil com o nome 'Administrador'"):
        service.criar_perfil(dto)
    repository.criar.assert_not_called()


def test_associar_usuario_sucesso(service, repository, perfil_model):
    """Deve associar um usuário a um perfil com sucesso."""
    # Arrange
    perfil_id = uuid.uuid4()
    usuario_id = uuid.uuid4()
    repository.buscar_por_id.return_value = perfil_model

    # Act
    service.associar_usuario(perfil_id, usuario_id)

    # Assert
    repository.buscar_por_id.assert_called_once_with(perfil_id)
    repository.associar_usuario.assert_called_once_with(perfil_id, usuario_id)


def test_associar_usuario_perfil_nao_encontrado(service, repository):
    """Deve falhar ao associar usuário a perfil inexistente."""
    # Arrange
    perfil_id = uuid.uuid4()
    usuario_id = uuid.uuid4()
    repository.buscar_por_id.return_value = None

    # Act/Assert
    with pytest.raises(ValueError, match=f"Perfil com ID '{perfil_id}' não encontrado"):
        service.associar_usuario(perfil_id, usuario_id)
    repository.associar_usuario.assert_not_called()


def test_associar_usuario_erro_integridade(service, repository, perfil_model):
    """Deve falhar ao associar usuário com erro de integridade."""
    # Arrange
    perfil_id = uuid.uuid4()
    usuario_id = uuid.uuid4()
    repository.buscar_por_id.return_value = perfil_model
    repository.associar_usuario.side_effect = ValueError("Usuário não encontrado")

    # Act/Assert
    with pytest.raises(ValueError, match="Usuário não encontrado"):
        service.associar_usuario(perfil_id, usuario_id) 