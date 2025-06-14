"""
Testes unitários para o objeto de valor Email.

Este módulo contém os testes unitários que validam o
comportamento do objeto de valor Email.
"""
import pytest

from src.joias.domain.shared.value_objects.email import Email


def test_criar_email_valido():
    """Deve criar um email com formato válido."""
    # Arrange
    valor = "joao@email.com"

    # Act
    email = Email(valor)

    # Assert
    assert str(email) == valor


def test_criar_email_vazio():
    """Deve lançar erro ao criar email vazio."""
    # Arrange
    valor = ""

    # Act & Assert
    with pytest.raises(ValueError) as exc:
        Email(valor)
    assert "vazio" in str(exc.value).lower()


def test_criar_email_invalido():
    """Deve lançar erro ao criar email com formato inválido."""
    # Arrange
    emails_invalidos = [
        "joao",
        "joao@",
        "@email.com",
        "joao@email",
        "joao@.com",
        "joao@email.",
        "joao email@email.com",
        "joao@email@com",
    ]

    # Act & Assert
    for valor in emails_invalidos:
        with pytest.raises(ValueError) as exc:
            Email(valor)
        assert "inválido" in str(exc.value).lower()


def test_email_minusculo():
    """Deve converter o email para minúsculas."""
    # Arrange
    valor = "JOAO@EMAIL.COM"
    esperado = "joao@email.com"

    # Act
    email = Email(valor)

    # Assert
    assert str(email) == esperado


def test_email_igual():
    """Deve considerar emails iguais mesmo com diferença de maiúsculas."""
    # Arrange
    email1 = Email("joao@email.com")
    email2 = Email("JOAO@EMAIL.COM")

    # Act & Assert
    assert email1 == email2


def test_email_diferente():
    """Deve considerar emails diferentes."""
    # Arrange
    email1 = Email("joao@email.com")
    email2 = Email("maria@email.com")

    # Act & Assert
    assert email1 != email2
