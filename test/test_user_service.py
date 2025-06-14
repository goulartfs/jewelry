"""
Testes para o serviço de usuários.

Este módulo contém os testes unitários para o serviço de usuários,
verificando a lógica de negócio e operações CRUD.
"""
import pytest
from uuid import uuid4

from joias.application.identity.user_service import UserService
from joias.domain.shared.value_objects.email import Email


def test_create_user(db_session):
    """Deve criar um usuário com sucesso."""
    service = UserService(db_session)
    email = Email("new@example.com")
    nome = "New User"
    senha = "password123"

    user = service.create_user(email, nome, senha)

    assert user is not None
    assert user.email == email
    assert user.nome == nome
    assert user.senha_hash != senha  # Senha deve estar hasheada


def test_create_user_duplicate_email(db_session, test_user):
    """Deve falhar ao criar usuário com email duplicado."""
    service = UserService(db_session)
    email = test_user.email
    nome = "Another User"
    senha = "password123"

    with pytest.raises(ValueError) as excinfo:
        service.create_user(email, nome, senha)
    assert "Email já cadastrado" in str(excinfo.value)


def test_get_user(db_session, test_user):
    """Deve buscar um usuário pelo ID."""
    service = UserService(db_session)
    user = service.get_user(str(test_user.id))

    assert user is not None
    assert user.id == test_user.id
    assert user.email == test_user.email


def test_get_nonexistent_user(db_session):
    """Deve retornar None para usuário inexistente."""
    service = UserService(db_session)
    user = service.get_user(str(uuid4()))

    assert user is None


def test_get_user_by_email(db_session, test_user):
    """Deve buscar um usuário pelo email."""
    service = UserService(db_session)
    user = service.get_user_by_email(test_user.email)

    assert user is not None
    assert user.id == test_user.id
    assert user.email == test_user.email


def test_get_user_by_nonexistent_email(db_session):
    """Deve retornar None para email inexistente."""
    service = UserService(db_session)
    email = Email("nonexistent@example.com")
    user = service.get_user_by_email(email)

    assert user is None


def test_list_users(db_session, test_user):
    """Deve listar usuários ativos."""
    service = UserService(db_session)
    users = service.list_users()

    assert len(users) > 0
    assert any(u.id == test_user.id for u in users)


def test_update_user_email(db_session, test_user):
    """Deve atualizar o email do usuário."""
    service = UserService(db_session)
    new_email = Email("updated@example.com")

    updated = service.update_user(
        user_id=str(test_user.id),
        email=new_email
    )

    assert updated.email == new_email


def test_update_user_nome(db_session, test_user):
    """Deve atualizar o nome do usuário."""
    service = UserService(db_session)
    new_nome = "Updated Name"

    updated = service.update_user(
        user_id=str(test_user.id),
        nome=new_nome
    )

    assert updated.nome == new_nome


def test_update_user_senha(db_session, test_user):
    """Deve atualizar a senha do usuário."""
    service = UserService(db_session)
    new_senha = "newpassword123"
    old_hash = test_user.senha_hash

    updated = service.update_user(
        user_id=str(test_user.id),
        senha=new_senha
    )

    assert updated.senha_hash != old_hash
    assert updated.senha_hash != new_senha  # Senha deve estar hasheada


def test_update_nonexistent_user(db_session):
    """Deve falhar ao atualizar usuário inexistente."""
    service = UserService(db_session)
    with pytest.raises(ValueError) as excinfo:
        service.update_user(
            user_id=str(uuid4()),
            nome="New Name"
        )
    assert "Usuário não encontrado" in str(excinfo.value)


def test_update_user_duplicate_email(db_session, test_user):
    """Deve falhar ao atualizar usuário com email duplicado."""
    # Cria outro usuário
    service = UserService(db_session)
    other_user = service.create_user(
        email=Email("other@example.com"),
        nome="Other User",
        senha="password123"
    )

    # Tenta atualizar o email do outro usuário para o email do test_user
    with pytest.raises(ValueError) as excinfo:
        service.update_user(
            user_id=str(other_user.id),
            email=test_user.email
        )
    assert "Email já cadastrado" in str(excinfo.value)


def test_delete_user(db_session, test_user):
    """Deve desativar um usuário."""
    service = UserService(db_session)
    service.delete_user(str(test_user.id))

    user = service.get_user(str(test_user.id))
    assert user is not None
    assert not user.ativo
    assert user.deleted_at is not None


def test_delete_nonexistent_user(db_session):
    """Deve falhar ao deletar usuário inexistente."""
    service = UserService(db_session)
    with pytest.raises(ValueError) as excinfo:
        service.delete_user(str(uuid4()))
    assert "Usuário não encontrado" in str(excinfo.value) 