"""
Testes para o serviço de usuário.
"""
from datetime import datetime
from unittest.mock import Mock
from uuid import UUID, uuid4

import pytest

from src.joias.application.identity.auth_service import AuthService
from src.joias.application.identity.usuario_service import UsuarioService
from src.joias.application.shared.exceptions import (
    EntidadeJaExisteError,
    EntidadeNaoEncontradaError,
    ValidacaoError,
)
from src.joias.domain.entities.usuario import Usuario
from src.joias.domain.shared.value_objects import Email


@pytest.fixture
def usuario_repository():
    """
    Fixture que retorna um mock do repositório de usuários.
    """
    return Mock()


@pytest.fixture
def auth_service():
    """
    Fixture que retorna um mock do serviço de autenticação.
    """
    return Mock()


@pytest.fixture
def usuario_service(usuario_repository, auth_service):
    """
    Fixture que retorna uma instância do serviço de usuários.
    """
    return UsuarioService(
        usuario_repository=usuario_repository,
        auth_service=auth_service,
    )


def test_criar_usuario_com_sucesso(usuario_service, usuario_repository, auth_service):
    """
    Testa a criação de um usuário com sucesso.
    """
    # Arrange
    nome = "John Doe"
    email = "john@doe.com"
    senha = "senha123"
    senha_hash = "hash123"

    auth_service.gerar_hash_senha.return_value = senha_hash
    usuario_repository.buscar_por_email.return_value = None
    usuario_repository.criar.return_value = Usuario(
        nome=nome,
        email=Email(email),
        senha_hash=senha_hash,
    )

    # Act
    usuario = usuario_service.criar_usuario(
        nome=nome,
        email=email,
        senha=senha,
    )

    # Assert
    assert usuario.nome == nome
    assert str(usuario.email) == email
    assert usuario.senha_hash == senha_hash
    assert usuario.ativo is True
    assert isinstance(usuario.data_criacao, datetime)

    auth_service.gerar_hash_senha.assert_called_once_with(senha)
    usuario_repository.buscar_por_email.assert_called_once_with(Email(email))
    usuario_repository.criar.assert_called_once()


def test_criar_usuario_com_email_invalido(usuario_service):
    """
    Testa a criação de um usuário com email inválido.
    """
    # Arrange
    nome = "John Doe"
    email = "email_invalido"
    senha = "senha123"

    # Act & Assert
    with pytest.raises(ValidacaoError):
        usuario_service.criar_usuario(
            nome=nome,
            email=email,
            senha=senha,
        )


def test_criar_usuario_com_email_ja_existente(usuario_service, usuario_repository):
    """
    Testa a criação de um usuário com email já existente.
    """
    # Arrange
    nome = "John Doe"
    email = "john@doe.com"
    senha = "senha123"

    usuario_repository.buscar_por_email.return_value = Usuario(
        nome=nome,
        email=Email(email),
        senha_hash="hash123",
    )

    # Act & Assert
    with pytest.raises(EntidadeJaExisteError):
        usuario_service.criar_usuario(
            nome=nome,
            email=email,
            senha=senha,
        )


def test_buscar_usuario_por_id_com_sucesso(usuario_service, usuario_repository):
    """
    Testa a busca de um usuário por ID com sucesso.
    """
    # Arrange
    id = str(uuid4())
    nome = "John Doe"
    email = "john@doe.com"
    senha_hash = "hash123"

    usuario_repository.buscar_por_id.return_value = Usuario(
        id=UUID(id),
        nome=nome,
        email=Email(email),
        senha_hash=senha_hash,
    )

    # Act
    usuario = usuario_service.buscar_usuario_por_id(id)

    # Assert
    assert str(usuario.id) == id
    assert usuario.nome == nome
    assert str(usuario.email) == email
    assert usuario.senha_hash == senha_hash

    usuario_repository.buscar_por_id.assert_called_once_with(id)


def test_buscar_usuario_por_id_nao_encontrado(usuario_service, usuario_repository):
    """
    Testa a busca de um usuário por ID não encontrado.
    """
    # Arrange
    id = str(uuid4())
    usuario_repository.buscar_por_id.return_value = None

    # Act & Assert
    with pytest.raises(EntidadeNaoEncontradaError):
        usuario_service.buscar_usuario_por_id(id)


def test_buscar_usuario_por_email_com_sucesso(usuario_service, usuario_repository):
    """
    Testa a busca de um usuário por email com sucesso.
    """
    # Arrange
    nome = "John Doe"
    email = "john@doe.com"
    senha_hash = "hash123"

    usuario_repository.buscar_por_email.return_value = Usuario(
        nome=nome,
        email=Email(email),
        senha_hash=senha_hash,
    )

    # Act
    usuario = usuario_service.buscar_usuario_por_email(email)

    # Assert
    assert usuario.nome == nome
    assert str(usuario.email) == email
    assert usuario.senha_hash == senha_hash

    usuario_repository.buscar_por_email.assert_called_once_with(Email(email))


def test_buscar_usuario_por_email_invalido(usuario_service):
    """
    Testa a busca de um usuário por email inválido.
    """
    # Arrange
    email = "email_invalido"

    # Act & Assert
    with pytest.raises(ValidacaoError):
        usuario_service.buscar_usuario_por_email(email)


def test_buscar_usuario_por_email_nao_encontrado(usuario_service, usuario_repository):
    """
    Testa a busca de um usuário por email não encontrado.
    """
    # Arrange
    email = "john@doe.com"
    usuario_repository.buscar_por_email.return_value = None

    # Act & Assert
    with pytest.raises(EntidadeNaoEncontradaError):
        usuario_service.buscar_usuario_por_email(email)


def test_listar_usuarios(usuario_service, usuario_repository):
    """
    Testa a listagem de usuários.
    """
    # Arrange
    usuarios = [
        Usuario(
            nome="John Doe",
            email=Email("john@doe.com"),
            senha_hash="hash123",
        ),
        Usuario(
            nome="Jane Doe",
            email=Email("jane@doe.com"),
            senha_hash="hash456",
        ),
    ]
    usuario_repository.listar.return_value = usuarios

    # Act
    resultado = usuario_service.listar_usuarios()

    # Assert
    assert len(resultado) == 2
    assert resultado == usuarios
    usuario_repository.listar.assert_called_once()


def test_atualizar_usuario_com_sucesso(usuario_service, usuario_repository, auth_service):
    """
    Testa a atualização de um usuário com sucesso.
    """
    # Arrange
    id = str(uuid4())
    nome = "John Doe"
    email = "john@doe.com"
    senha = "senha123"
    senha_hash = "hash123"
    ativo = False

    usuario_repository.buscar_por_id.return_value = Usuario(
        id=UUID(id),
        nome="Old Name",
        email=Email("old@email.com"),
        senha_hash="oldhash",
        ativo=True,
    )
    usuario_repository.buscar_por_email.return_value = None
    auth_service.gerar_hash_senha.return_value = senha_hash
    usuario_repository.atualizar.return_value = Usuario(
        id=UUID(id),
        nome=nome,
        email=Email(email),
        senha_hash=senha_hash,
        ativo=ativo,
    )

    # Act
    usuario = usuario_service.atualizar_usuario(
        id=id,
        nome=nome,
        email=email,
        senha=senha,
        ativo=ativo,
    )

    # Assert
    assert str(usuario.id) == id
    assert usuario.nome == nome
    assert str(usuario.email) == email
    assert usuario.senha_hash == senha_hash
    assert usuario.ativo == ativo

    usuario_repository.buscar_por_id.assert_called_once_with(id)
    usuario_repository.buscar_por_email.assert_called_once_with(Email(email))
    auth_service.gerar_hash_senha.assert_called_once_with(senha)
    usuario_repository.atualizar.assert_called_once()


def test_atualizar_usuario_nao_encontrado(usuario_service, usuario_repository):
    """
    Testa a atualização de um usuário não encontrado.
    """
    # Arrange
    id = str(uuid4())
    usuario_repository.buscar_por_id.return_value = None

    # Act & Assert
    with pytest.raises(EntidadeNaoEncontradaError):
        usuario_service.atualizar_usuario(
            id=id,
            nome="John Doe",
        )


def test_atualizar_usuario_com_email_ja_existente(usuario_service, usuario_repository):
    """
    Testa a atualização de um usuário com email já existente.
    """
    # Arrange
    id = str(uuid4())
    email = "john@doe.com"

    usuario_repository.buscar_por_id.return_value = Usuario(
        id=UUID(id),
        nome="Old Name",
        email=Email("old@email.com"),
        senha_hash="oldhash",
    )
    usuario_repository.buscar_por_email.return_value = Usuario(
        id=uuid4(),
        nome="Other User",
        email=Email(email),
        senha_hash="hash123",
    )

    # Act & Assert
    with pytest.raises(EntidadeJaExisteError):
        usuario_service.atualizar_usuario(
            id=id,
            email=email,
        )


def test_excluir_usuario_com_sucesso(usuario_service, usuario_repository):
    """
    Testa a exclusão de um usuário com sucesso.
    """
    # Arrange
    id = str(uuid4())
    usuario = Usuario(
        id=UUID(id),
        nome="John Doe",
        email=Email("john@doe.com"),
        senha_hash="hash123",
    )
    usuario_repository.buscar_por_id.return_value = usuario

    # Act
    usuario_service.excluir_usuario(id)

    # Assert
    usuario_repository.buscar_por_id.assert_called_once_with(id)
    usuario_repository.excluir.assert_called_once_with(usuario)


def test_excluir_usuario_nao_encontrado(usuario_service, usuario_repository):
    """
    Testa a exclusão de um usuário não encontrado.
    """
    # Arrange
    id = str(uuid4())
    usuario_repository.buscar_por_id.return_value = None

    # Act & Assert
    with pytest.raises(EntidadeNaoEncontradaError):
        usuario_service.excluir_usuario(id) 