"""
Testes para o objeto de valor Email.

Este módulo contém os testes unitários para a classe Email,
verificando a validação e comportamento do objeto de valor.
"""
import pytest

from joias.domain.shared.value_objects.email import Email


def test_criar_email_valido():
    """Deve criar um email válido."""
    email = Email("user@example.com")
    assert str(email) == "user@example.com"


def test_criar_email_vazio():
    """Deve lançar erro ao criar email vazio."""
    with pytest.raises(ValueError) as excinfo:
        Email("")
    assert "O email não pode estar vazio" in str(excinfo.value)


def test_criar_email_invalido():
    """Deve lançar erro ao criar email inválido."""
    emails_invalidos = [
        "user",
        "user@",
        "@example.com",
        "user@.com",
        "user@example.",
        "user@example",
        "user.example.com",
        "@",
        "user@example..com",
    ]

    for email in emails_invalidos:
        with pytest.raises(ValueError) as excinfo:
            Email(email)
        assert "Email inválido" in str(excinfo.value)


def test_criar_email_com_caracteres_especiais():
    """Deve criar email com caracteres especiais válidos."""
    emails_validos = [
        "user.name@example.com",
        "user+tag@example.com",
        "user-name@example.com",
        "user_name@example.com",
        "user123@example.com",
        "user@sub.example.com",
    ]

    for email in emails_validos:
        assert str(Email(email)) == email


def test_comparacao_emails():
    """Deve comparar emails corretamente."""
    email1 = Email("user@example.com")
    email2 = Email("user@example.com")
    email3 = Email("other@example.com")

    assert email1 == email2
    assert email1 != email3
    assert hash(email1) == hash(email2)
    assert hash(email1) != hash(email3) 