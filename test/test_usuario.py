"""
Testes para a entidade de usuário.

Este módulo contém os testes unitários para a entidade de usuário,
verificando seu comportamento e regras de negócio.
"""
import pytest
from datetime import datetime
from uuid import UUID, uuid4

from joias.domain.identity.entities.usuario import Usuario
from joias.domain.shared.value_objects.email import Email


@pytest.fixture
def usuario():
    """Fixture que cria um usuário para testes."""
    return Usuario(
        id=uuid4(),
        email=Email("test@example.com"),
        nome="Test User",
        senha_hash="hash123",
        ativo=True
    )


def test_criar_usuario(usuario):
    """Deve criar um usuário com atributos corretos."""
    assert usuario.email == Email("test@example.com")
    assert usuario.nome == "Test User"
    assert usuario.senha_hash == "hash123"
    assert usuario.ativo is True
    assert usuario.empresa_id is None
    assert len(usuario.perfis) == 0


def test_ativar_usuario(usuario):
    """Deve ativar um usuário inativo."""
    usuario.desativar()
    assert usuario.ativo is False
    assert usuario.deleted_at is not None

    usuario.ativar()
    assert usuario.ativo is True
    assert usuario.deleted_at is None


def test_desativar_usuario(usuario):
    """Deve desativar um usuário ativo."""
    assert usuario.ativo is True
    assert usuario.deleted_at is None

    usuario.desativar()
    assert usuario.ativo is False
    assert usuario.deleted_at is not None


def test_adicionar_perfil(usuario):
    """Deve adicionar um perfil ao usuário."""
    perfil_id = uuid4()
    assert perfil_id not in usuario.perfis

    usuario.adicionar_perfil(perfil_id)
    assert perfil_id in usuario.perfis


def test_remover_perfil(usuario):
    """Deve remover um perfil do usuário."""
    perfil_id = uuid4()
    usuario.adicionar_perfil(perfil_id)
    assert perfil_id in usuario.perfis

    usuario.remover_perfil(perfil_id)
    assert perfil_id not in usuario.perfis


def test_atualizar_email(usuario):
    """Deve atualizar o email do usuário."""
    novo_email = Email("new@example.com")
    assert usuario.email != novo_email

    usuario.atualizar_email(novo_email)
    assert usuario.email == novo_email


def test_atualizar_nome(usuario):
    """Deve atualizar o nome do usuário."""
    novo_nome = "New Name"
    assert usuario.nome != novo_nome

    usuario.atualizar_nome(novo_nome)
    assert usuario.nome == novo_nome


def test_atualizar_senha(usuario):
    """Deve atualizar a senha do usuário."""
    nova_senha = "newhash123"
    assert usuario.senha_hash != nova_senha

    usuario.atualizar_senha(nova_senha)
    assert usuario.senha_hash == nova_senha


def test_vincular_empresa(usuario):
    """Deve vincular uma empresa ao usuário."""
    empresa_id = uuid4()
    assert usuario.empresa_id is None

    usuario.vincular_empresa(empresa_id)
    assert usuario.empresa_id == empresa_id


def test_desvincular_empresa(usuario):
    """Deve desvincular a empresa do usuário."""
    empresa_id = uuid4()
    usuario.vincular_empresa(empresa_id)
    assert usuario.empresa_id == empresa_id

    usuario.desvincular_empresa()
    assert usuario.empresa_id is None


def test_str_representation(usuario):
    """Deve retornar uma representação em string correta."""
    expected = "Test User (test@example.com) - ativo"
    assert str(usuario) == expected

    usuario.desativar()
    expected = "Test User (test@example.com) - inativo" 