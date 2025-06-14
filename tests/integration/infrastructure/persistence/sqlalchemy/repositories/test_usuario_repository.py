"""
Testes de integração para o repositório de usuários.

Este módulo contém os testes que validam a integração
do repositório de usuários com o banco de dados.
"""
from datetime import datetime
from uuid import uuid4

import pytest

from src.joias.domain.identity.entities.usuario import Usuario
from src.joias.domain.shared.value_objects.email import Email
from src.joias.infrastructure.persistence.sqlalchemy.repositories.usuario_repository import (
    SQLUsuarioRepository,
)


@pytest.fixture
def usuario_valido() -> Usuario:
    """Fixture que retorna um usuário válido."""
    return Usuario(
        nome="João da Silva",
        email=Email("joao@email.com"),
        senha_hashed="hash123",
        data_criacao=datetime.now(),
    )


def test_criar_usuario(db_session, usuario_valido):
    """Deve criar um usuário no banco de dados."""
    # Arrange
    repository = SQLUsuarioRepository(db_session)

    # Act
    usuario = repository.criar(usuario_valido)

    # Assert
    assert usuario.id is not None
    assert usuario.nome == usuario_valido.nome
    assert usuario.email == usuario_valido.email
    assert usuario.senha_hashed == usuario_valido.senha_hashed
    assert usuario.ativo is True


def test_criar_usuario_email_duplicado(db_session, usuario_valido):
    """Deve lançar erro ao criar usuário com email duplicado."""
    # Arrange
    repository = SQLUsuarioRepository(db_session)
    repository.criar(usuario_valido)

    # Act & Assert
    with pytest.raises(ValueError) as exc:
        repository.criar(usuario_valido)
    assert "já cadastrado" in str(exc.value).lower()


def test_buscar_usuario_por_id(db_session, usuario_valido):
    """Deve buscar um usuário pelo ID."""
    # Arrange
    repository = SQLUsuarioRepository(db_session)
    criado = repository.criar(usuario_valido)

    # Act
    encontrado = repository.buscar_por_id(str(criado.id))

    # Assert
    assert encontrado is not None
    assert encontrado.id == criado.id
    assert encontrado.nome == criado.nome
    assert encontrado.email == criado.email


def test_buscar_usuario_por_id_inexistente(db_session):
    """Deve retornar None ao buscar usuário inexistente."""
    # Arrange
    repository = SQLUsuarioRepository(db_session)

    # Act
    encontrado = repository.buscar_por_id(str(uuid4()))

    # Assert
    assert encontrado is None


def test_buscar_usuario_por_email(db_session, usuario_valido):
    """Deve buscar um usuário pelo email."""
    # Arrange
    repository = SQLUsuarioRepository(db_session)
    criado = repository.criar(usuario_valido)

    # Act
    encontrado = repository.buscar_por_email(criado.email)

    # Assert
    assert encontrado is not None
    assert encontrado.id == criado.id
    assert encontrado.nome == criado.nome
    assert encontrado.email == criado.email


def test_buscar_usuario_por_email_inexistente(db_session):
    """Deve retornar None ao buscar email inexistente."""
    # Arrange
    repository = SQLUsuarioRepository(db_session)

    # Act
    encontrado = repository.buscar_por_email(Email("inexistente@email.com"))

    # Assert
    assert encontrado is None


def test_listar_usuarios(db_session, usuario_valido):
    """Deve listar usuários com paginação."""
    # Arrange
    repository = SQLUsuarioRepository(db_session)

    # Cria 15 usuários
    for i in range(15):
        usuario = Usuario(
            nome=f"Usuário {i}",
            email=Email(f"usuario{i}@email.com"),
            senha_hashed="hash123",
        )
        repository.criar(usuario)

    # Act
    pagina1 = repository.listar(pagina=1, tamanho=10)
    pagina2 = repository.listar(pagina=2, tamanho=10)

    # Assert
    assert len(pagina1) == 10
    assert len(pagina2) == 5


def test_listar_usuarios_filtro_email(db_session, usuario_valido):
    """Deve filtrar usuários por email."""
    # Arrange
    repository = SQLUsuarioRepository(db_session)
    repository.criar(usuario_valido)

    # Act
    encontrados = repository.listar(email="joao@email.com")
    nao_encontrados = repository.listar(email="maria@email.com")

    # Assert
    assert len(encontrados) == 1
    assert len(nao_encontrados) == 0
    assert encontrados[0].email == usuario_valido.email


def test_listar_usuarios_filtro_nome(db_session, usuario_valido):
    """Deve filtrar usuários por nome."""
    # Arrange
    repository = SQLUsuarioRepository(db_session)
    repository.criar(usuario_valido)

    # Act
    encontrados = repository.listar(nome="João")
    nao_encontrados = repository.listar(nome="Maria")

    # Assert
    assert len(encontrados) == 1
    assert len(nao_encontrados) == 0
    assert encontrados[0].nome == usuario_valido.nome


def test_atualizar_usuario(db_session, usuario_valido):
    """Deve atualizar um usuário existente."""
    # Arrange
    repository = SQLUsuarioRepository(db_session)
    criado = repository.criar(usuario_valido)

    # Modifica os dados
    novo_nome = "João Silva"
    novo_email = Email("joao.silva@email.com")

    usuario_atualizado = Usuario(
        nome=novo_nome,
        email=novo_email,
        senha_hashed=criado.senha_hashed,
        data_criacao=criado.data_criacao,
        ativo=False,
    )

    # Act
    atualizado = repository.atualizar(usuario_atualizado)

    # Assert
    assert atualizado.nome == novo_nome
    assert atualizado.email == novo_email
    assert atualizado.ativo is False


def test_atualizar_usuario_inexistente(db_session, usuario_valido):
    """Deve lançar erro ao atualizar usuário inexistente."""
    # Arrange
    repository = SQLUsuarioRepository(db_session)

    # Act & Assert
    with pytest.raises(ValueError) as exc:
        repository.atualizar(usuario_valido)
    assert "não encontrado" in str(exc.value).lower()


def test_excluir_usuario(db_session, usuario_valido):
    """Deve excluir um usuário existente."""
    # Arrange
    repository = SQLUsuarioRepository(db_session)
    criado = repository.criar(usuario_valido)

    # Act
    repository.excluir(str(criado.id))
    encontrado = repository.buscar_por_id(str(criado.id))

    # Assert
    assert encontrado is None


def test_excluir_usuario_inexistente(db_session):
    """Deve lançar erro ao excluir usuário inexistente."""
    # Arrange
    repository = SQLUsuarioRepository(db_session)

    # Act & Assert
    with pytest.raises(ValueError) as exc:
        repository.excluir(str(uuid4()))
    assert "não encontrado" in str(exc.value).lower()
