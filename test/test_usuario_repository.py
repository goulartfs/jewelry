"""
Testes para o repositório de usuários.

Este módulo contém os testes unitários para o repositório de usuários,
verificando as operações de persistência e recuperação.
"""
import pytest
from uuid import UUID

from joias.domain.identity.entities.usuario import Usuario
from joias.domain.shared.value_objects.email import Email
from joias.infrastructure.persistence.sqlalchemy.repositories.usuario_repository import UsuarioRepository


def test_proximo_id(db_session):
    """Deve gerar um novo UUID válido."""
    repo = UsuarioRepository(db_session)
    id = repo.proximo_id()

    assert isinstance(id, UUID)
    assert str(id) != "00000000-0000-0000-0000-000000000000"


def test_salvar_usuario(db_session):
    """Deve salvar um usuário corretamente."""
    repo = UsuarioRepository(db_session)
    usuario = Usuario(
        id=repo.proximo_id(),
        email=Email("test@example.com"),
        nome="Test User",
        senha_hash="hash123"
    )

    saved = repo.salvar(usuario)

    assert saved.id == usuario.id
    assert saved.email == usuario.email
    assert saved.nome == usuario.nome
    assert saved.senha_hash == usuario.senha_hash


def test_buscar_por_id(db_session, test_user):
    """Deve buscar um usuário pelo ID."""
    repo = UsuarioRepository(db_session)
    found = repo.buscar_por_id(test_user.id)

    assert found is not None
    assert found.id == test_user.id
    assert found.email == test_user.email


def test_buscar_por_id_inexistente(db_session):
    """Deve retornar None para ID inexistente."""
    repo = UsuarioRepository(db_session)
    found = repo.buscar_por_id(UUID("00000000-0000-0000-0000-000000000000"))

    assert found is None


def test_buscar_por_email(db_session, test_user):
    """Deve buscar um usuário pelo email."""
    repo = UsuarioRepository(db_session)
    found = repo.buscar_por_email(test_user.email)

    assert found is not None
    assert found.id == test_user.id
    assert found.email == test_user.email


def test_buscar_por_email_inexistente(db_session):
    """Deve retornar None para email inexistente."""
    repo = UsuarioRepository(db_session)
    found = repo.buscar_por_email(Email("nonexistent@example.com"))

    assert found is None


def test_listar_usuarios(db_session, test_user):
    """Deve listar todos os usuários ativos."""
    repo = UsuarioRepository(db_session)
    users = repo.listar(apenas_ativos=True)

    assert len(users) > 0
    assert any(u.id == test_user.id for u in users)


def test_listar_usuarios_inativos(db_session, test_user):
    """Deve listar usuários inativos quando solicitado."""
    repo = UsuarioRepository(db_session)
    
    # Desativa o usuário de teste
    test_user.desativar()
    repo.salvar(test_user)

    users = repo.listar(apenas_ativos=False)
    active_users = repo.listar(apenas_ativos=True)

    assert len(users) > len(active_users)
    assert any(u.id == test_user.id for u in users)
    assert not any(u.id == test_user.id for u in active_users)


def test_excluir_usuario(db_session, test_user):
    """Deve excluir um usuário corretamente."""
    repo = UsuarioRepository(db_session)
    success = repo.excluir(test_user.id)

    assert success
    assert repo.buscar_por_id(test_user.id) is None


def test_excluir_usuario_inexistente(db_session):
    """Deve retornar False ao tentar excluir usuário inexistente."""
    repo = UsuarioRepository(db_session)
    success = repo.excluir(UUID("00000000-0000-0000-0000-000000000000"))

    assert not success 