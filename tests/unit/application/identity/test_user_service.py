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
    AtualizarUsuarioDTO,
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


def test_atualizar_usuario(repository_mock, usuario_mock):
    """Deve atualizar um usuário com sucesso."""
    # Arrange
    service = UserService(repository_mock)
    repository_mock.buscar_por_id.return_value = usuario_mock
    repository_mock.buscar_por_email.return_value = None
    repository_mock.atualizar.return_value = Usuario(
        id=usuario_mock.id,
        nome="João Silva",
        email=Email("joao.silva@email.com"),
        senha_hashed="hash123",
        data_criacao=usuario_mock.data_criacao,
        ativo=True
    )
    
    dto = AtualizarUsuarioDTO(
        id=str(usuario_mock.id),
        nome="João Silva",
        email="joao.silva@email.com",
        ativo=True
    )
    
    # Act
    resultado = service.atualizar_usuario(dto)
    
    # Assert
    assert isinstance(resultado, UsuarioDTO)
    assert resultado.nome == "João Silva"
    assert resultado.email == "joao.silva@email.com"
    assert resultado.ativo is True
    repository_mock.atualizar.assert_called_once()


def test_atualizar_usuario_inexistente(repository_mock):
    """Deve lançar erro ao atualizar usuário inexistente."""
    # Arrange
    service = UserService(repository_mock)
    repository_mock.buscar_por_id.return_value = None
    
    dto = AtualizarUsuarioDTO(
        id="123",
        nome="João Silva",
        email="joao.silva@email.com",
        ativo=True
    )
    
    # Act & Assert
    with pytest.raises(ValueError) as exc:
        service.atualizar_usuario(dto)
    assert "não encontrado" in str(exc.value).lower()
    repository_mock.atualizar.assert_not_called()


def test_atualizar_usuario_email_duplicado(repository_mock, usuario_mock):
    """Deve lançar erro ao atualizar usuário com email duplicado."""
    # Arrange
    service = UserService(repository_mock)
    repository_mock.buscar_por_id.return_value = usuario_mock
    
    # Simula outro usuário com o mesmo email
    outro_usuario = Usuario(
        nome="Outro Usuário",
        email=Email("joao.silva@email.com"),
        senha_hashed="hash123"
    )
    repository_mock.buscar_por_email.return_value = outro_usuario
    
    dto = AtualizarUsuarioDTO(
        id=str(usuario_mock.id),
        nome="João Silva",
        email="joao.silva@email.com",
        ativo=True
    )
    
    # Act & Assert
    with pytest.raises(ValueError) as exc:
        service.atualizar_usuario(dto)
    assert "já cadastrado" in str(exc.value).lower()
    repository_mock.atualizar.assert_not_called()


def test_atualizar_usuario_parcial(repository_mock, usuario_mock):
    """Deve atualizar parcialmente um usuário."""
    # Arrange
    service = UserService(repository_mock)
    repository_mock.buscar_por_id.return_value = usuario_mock
    repository_mock.atualizar.return_value = Usuario(
        id=usuario_mock.id,
        nome="João Silva",
        email=usuario_mock.email,
        senha_hashed=usuario_mock.senha_hashed,
        data_criacao=usuario_mock.data_criacao,
        ativo=usuario_mock.ativo
    )
    
    dto = AtualizarUsuarioDTO(
        id=str(usuario_mock.id),
        nome="João Silva"  # Atualiza apenas o nome
    )
    
    # Act
    resultado = service.atualizar_usuario(dto)
    
    # Assert
    assert isinstance(resultado, UsuarioDTO)
    assert resultado.nome == "João Silva"
    assert resultado.email == str(usuario_mock.email)
    assert resultado.ativo == usuario_mock.ativo
    repository_mock.atualizar.assert_called_once()


def test_excluir_usuario(repository_mock, usuario_mock):
    """Deve excluir um usuário com sucesso."""
    # Arrange
    service = UserService(repository_mock)
    repository_mock.buscar_por_id.return_value = usuario_mock
    
    # Act
    service.excluir_usuario(str(usuario_mock.id))
    
    # Assert
    repository_mock.excluir.assert_called_once_with(str(usuario_mock.id))


def test_excluir_usuario_inexistente(repository_mock):
    """Deve lançar erro ao excluir usuário inexistente."""
    # Arrange
    service = UserService(repository_mock)
    repository_mock.buscar_por_id.return_value = None
    
    # Act & Assert
    with pytest.raises(ValueError) as exc:
        service.excluir_usuario("123")
    assert "não encontrado" in str(exc.value).lower()
    repository_mock.excluir.assert_not_called()


def test_excluir_usuario_com_dependencias(repository_mock, usuario_mock):
    """Deve lançar erro ao excluir usuário com dependências."""
    # Arrange
    service = UserService(repository_mock)
    repository_mock.buscar_por_id.return_value = usuario_mock
    repository_mock.excluir.side_effect = ValueError("Usuário possui pedidos ativos")
    
    # Act & Assert
    with pytest.raises(ValueError) as exc:
        service.excluir_usuario(str(usuario_mock.id))
    assert "possui pedidos" in str(exc.value).lower()
    repository_mock.excluir.assert_called_once_with(str(usuario_mock.id))
