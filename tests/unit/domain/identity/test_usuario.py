"""
Testes unitários para a entidade Usuario.

Este módulo contém os testes unitários que validam o
comportamento da entidade Usuario.
"""
from datetime import datetime

import pytest

from src.joias.domain.identity.entities.usuario import Usuario
from src.joias.domain.shared.value_objects.email import Email


def test_criar_usuario_valido():
    """Deve criar um usuário com dados válidos."""
    # Arrange
    nome = "João da Silva"
    email = Email("joao@email.com")
    senha_hashed = "hash123"
    data_criacao = datetime.now()

    # Act
    usuario = Usuario(
        nome=nome, email=email, senha_hashed=senha_hashed, data_criacao=data_criacao
    )

    # Assert
    assert usuario.nome == nome
    assert usuario.email == email
    assert usuario.senha_hashed == senha_hashed
    assert usuario.data_criacao == data_criacao
    assert usuario.ativo is True


def test_criar_usuario_nome_vazio():
    """Deve lançar erro ao criar usuário com nome vazio."""
    # Arrange
    nome = ""
    email = Email("joao@email.com")
    senha_hashed = "hash123"

    # Act & Assert
    with pytest.raises(ValueError) as exc:
        Usuario(nome=nome, email=email, senha_hashed=senha_hashed)
    assert "nome" in str(exc.value).lower()


def test_criar_usuario_nome_espacos():
    """Deve lançar erro ao criar usuário com nome só com espaços."""
    # Arrange
    nome = "   "
    email = Email("joao@email.com")
    senha_hashed = "hash123"

    # Act & Assert
    with pytest.raises(ValueError) as exc:
        Usuario(nome=nome, email=email, senha_hashed=senha_hashed)
    assert "nome" in str(exc.value).lower()


def test_desativar_usuario():
    """Deve desativar um usuário ativo."""
    # Arrange
    usuario = Usuario(
        nome="João da Silva", email=Email("joao@email.com"), senha_hashed="hash123"
    )
    assert usuario.ativo is True

    # Act
    usuario.desativar()

    # Assert
    assert usuario.ativo is False


def test_desativar_usuario_ja_inativo():
    """Não deve ter efeito ao desativar um usuário já inativo."""
    # Arrange
    usuario = Usuario(
        nome="João da Silva",
        email=Email("joao@email.com"),
        senha_hashed="hash123",
        ativo=False,
    )
    assert usuario.ativo is False

    # Act
    usuario.desativar()

    # Assert
    assert usuario.ativo is False


def test_ativar_usuario():
    """Deve ativar um usuário inativo."""
    # Arrange
    usuario = Usuario(
        nome="João da Silva",
        email=Email("joao@email.com"),
        senha_hashed="hash123",
        ativo=False,
    )
    assert usuario.ativo is False

    # Act
    usuario.ativar()

    # Assert
    assert usuario.ativo is True


def test_ativar_usuario_ja_ativo():
    """Não deve ter efeito ao ativar um usuário já ativo."""
    # Arrange
    usuario = Usuario(
        nome="João da Silva", email=Email("joao@email.com"), senha_hashed="hash123"
    )
    assert usuario.ativo is True

    # Act
    usuario.ativar()

    # Assert
    assert usuario.ativo is True
