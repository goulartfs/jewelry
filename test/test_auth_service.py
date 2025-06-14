"""
Testes para o serviço de autenticação.

Este módulo contém os testes unitários para o serviço de autenticação,
verificando a geração de tokens, autenticação e validação de senhas.
"""
import pytest
from datetime import timedelta
from uuid import uuid4

from joias.application.identity.auth_service import AuthService
from joias.domain.identity.entities.usuario import Usuario
from joias.domain.shared.value_objects.email import Email


def test_verify_password(db_session):
    """Deve verificar senha corretamente."""
    auth_service = AuthService(db_session)
    password = "testpass123"
    hashed = auth_service.get_password_hash(password)

    assert auth_service.verify_password(password, hashed)
    assert not auth_service.verify_password("wrongpass", hashed)


def test_get_password_hash(db_session):
    """Deve gerar hash de senha corretamente."""
    auth_service = AuthService(db_session)
    password = "testpass123"
    hashed = auth_service.get_password_hash(password)

    assert hashed != password
    assert len(hashed) > 50  # Bcrypt hash tem pelo menos 50 caracteres


def test_authenticate_success(db_session, test_user):
    """Deve autenticar usuário com credenciais corretas."""
    auth_service = AuthService(db_session)
    email = Email("test@example.com")
    password = "testpass123"

    user = auth_service.authenticate(email, password)
    assert user is not None
    assert user.email == email


def test_authenticate_wrong_password(db_session, test_user):
    """Não deve autenticar usuário com senha incorreta."""
    auth_service = AuthService(db_session)
    email = Email("test@example.com")
    password = "wrongpass"

    user = auth_service.authenticate(email, password)
    assert user is None


def test_authenticate_nonexistent_user(db_session):
    """Não deve autenticar usuário inexistente."""
    auth_service = AuthService(db_session)
    email = Email("nonexistent@example.com")
    password = "testpass123"

    user = auth_service.authenticate(email, password)
    assert user is None


def test_create_access_token(db_session):
    """Deve criar token de acesso corretamente."""
    auth_service = AuthService(db_session)
    user_id = str(uuid4())
    expires_delta = timedelta(minutes=30)

    token = auth_service.create_access_token(
        data={"sub": user_id},
        expires_delta=expires_delta
    )

    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0


def test_get_user(db_session, test_user):
    """Deve retornar usuário pelo ID."""
    auth_service = AuthService(db_session)
    user = auth_service.get_user(str(test_user.id))

    assert user is not None
    assert user.id == test_user.id
    assert user.email == test_user.email


def test_get_nonexistent_user(db_session):
    """Deve retornar None para usuário inexistente."""
    auth_service = AuthService(db_session)
    user = auth_service.get_user(str(uuid4()))

    assert user is None 