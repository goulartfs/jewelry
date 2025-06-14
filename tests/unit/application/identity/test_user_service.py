"""
Testes unitários para o serviço de usuários.

Este módulo contém os testes que validam o comportamento
do serviço de usuários da aplicação.
"""
from datetime import datetime
from unittest.mock import Mock

import pytest

from src.joias.application.identity.user_service import (
    CriarUsuarioDTO,
    UserService,
    UsuarioDTO,
)
from src.joias.domain.identity.entities.usuario import Usuario
from src.joias.domain.shared.value_objects.email import Email


@pytest.fixture
def usuario_mock() -> Usuario:
    """Fixture que retorna um mock de usuário."""
    return Usuario(
        nome="João da Silva",
        email=Email("joao@email.com"),
        senha_hashed="hash123",
        data_criacao=datetime.now(),
    )


@pytest.fixture
def repository_mock(usuario_mock) -> Mock:
    """Fixture que retorna um mock do repositório."""
    repository = Mock()
    repository.criar.return_value = usuario_mock
    repository.buscar_por_id.return_value = usuario_mock
    repository.buscar_por_email.return_value = None
    repository.listar.return_value = [usuario_mock]
    return repository


def test_criar_usuario(repository_mock, usuario_mock):
    """Deve criar um usuário com sucesso."""
    # Arrange
    service = UserService(repository_mock)
    dto = CriarUsuarioDTO(
        nome="João da Silva", email="joao@email.com", senha="senha123"
    )

    # Act
    resultado = service.criar_usuario(dto)

    # Assert
    assert isinstance(resultado, UsuarioDTO)
    assert resultado.nome == usuario_mock.nome
    assert resultado.email == str(usuario_mock.email)
    assert resultado.ativo == usuario_mock.ativo
    repository_mock.criar.assert_called_once()


def test_criar_usuario_email_duplicado(repository_mock):
    """Deve lançar erro ao criar usuário com email duplicado."""
    # Arrange
    repository_mock.buscar_por_email.return_value = Usuario(
        nome="Outro Usuário", email=Email("joao@email.com"), senha_hashed="hash123"
    )

    service = UserService(repository_mock)
    dto = CriarUsuarioDTO(
        nome="João da Silva", email="joao@email.com", senha="senha123"
    )

    # Act & Assert
    with pytest.raises(ValueError) as exc:
        service.criar_usuario(dto)
    assert "já cadastrado" in str(exc.value).lower()
    repository_mock.criar.assert_not_called()


def test_buscar_usuario(repository_mock, usuario_mock):
    """Deve buscar um usuário pelo ID."""
    # Arrange
    service = UserService(repository_mock)

    # Act
    resultado = service.buscar_usuario("123")

    # Assert
    assert isinstance(resultado, UsuarioDTO)
    assert resultado.nome == usuario_mock.nome
    assert resultado.email == str(usuario_mock.email)
    repository_mock.buscar_por_id.assert_called_once_with("123")


def test_buscar_usuario_inexistente(repository_mock):
    """Deve retornar None ao buscar usuário inexistente."""
    # Arrange
    repository_mock.buscar_por_id.return_value = None
    service = UserService(repository_mock)

    # Act
    resultado = service.buscar_usuario("123")

    # Assert
    assert resultado is None
    repository_mock.buscar_por_id.assert_called_once_with("123")


def test_listar_usuarios(repository_mock, usuario_mock):
    """Deve listar usuários com paginação e filtros."""
    # Arrange
    service = UserService(repository_mock)

    # Act
    resultado = service.listar_usuarios(
        pagina=1, tamanho=10, email="joao@email.com", nome="João"
    )

    # Assert
    assert isinstance(resultado, list)
    assert len(resultado) == 1
    assert isinstance(resultado[0], UsuarioDTO)
    assert resultado[0].nome == usuario_mock.nome
    repository_mock.listar.assert_called_once_with(
        pagina=1, tamanho=10, email="joao@email.com", nome="João"
    )
