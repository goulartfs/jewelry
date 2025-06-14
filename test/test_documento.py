"""
Testes para o objeto de valor Documento.

Este módulo contém os testes unitários para o objeto de valor Documento,
verificando se todas as validações e comportamentos funcionam conforme
esperado.
"""
import pytest

from src.joias.domain.catalogo.entities.fornecedor import Documento


def test_criar_documento_cnpj_valido():
    """Testa a criação de um documento CNPJ válido."""
    # Act
    documento = Documento(
        numero="12345678901234",
        tipo="CNPJ"
    )

    # Assert
    assert documento.numero == "12345678901234"
    assert documento.tipo == "CNPJ"


def test_criar_documento_cpf_valido():
    """Testa a criação de um documento CPF válido."""
    # Act
    documento = Documento(
        numero="12345678901",
        tipo="CPF"
    )

    # Assert
    assert documento.numero == "12345678901"
    assert documento.tipo == "CPF"


def test_criar_documento_sem_numero():
    """Testa a tentativa de criar um documento sem número."""
    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        Documento(
            numero="",
            tipo="CNPJ"
        )
    assert "O número do documento não pode estar vazio" in str(exc_info.value)


def test_criar_documento_sem_tipo():
    """Testa a tentativa de criar um documento sem tipo."""
    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        Documento(
            numero="12345678901234",
            tipo=""
        )
    assert "O tipo do documento não pode estar vazio" in str(exc_info.value)


def test_criar_documento_cnpj_invalido():
    """Testa a tentativa de criar um documento CNPJ com número inválido."""
    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        Documento(
            numero="123456789",
            tipo="CNPJ"
        )
    assert "CNPJ deve ter 14 dígitos" in str(exc_info.value)


def test_criar_documento_cpf_invalido():
    """Testa a tentativa de criar um documento CPF com número inválido."""
    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        Documento(
            numero="123456789",
            tipo="CPF"
        )
    assert "CPF deve ter 11 dígitos" in str(exc_info.value)


def test_criar_documento_tipo_maiusculo():
    """Testa se o tipo é convertido para maiúsculas."""
    # Act
    documento = Documento(
        numero="12345678901234",
        tipo="cnpj"
    )

    # Assert
    assert documento.tipo == "CNPJ"


def test_criar_documento_numero_com_mascara():
    """Testa se o número com máscara é aceito e formatado corretamente."""
    # Act
    documento = Documento(
        numero="12.345.678/0001-34",
        tipo="CNPJ"
    )

    # Assert
    assert documento.numero == "12345678901234"


def test_criar_documento_cnpj_str():
    """Testa a representação string de um documento CNPJ."""
    # Arrange
    documento = Documento(
        numero="12345678901234",
        tipo="CNPJ"
    )

    # Act
    documento_str = str(documento)

    # Assert
    assert documento_str == "CNPJ: 12.345.678/0001-34"


def test_criar_documento_cpf_str():
    """Testa a representação string de um documento CPF."""
    # Arrange
    documento = Documento(
        numero="12345678901",
        tipo="CPF"
    )

    # Act
    documento_str = str(documento)

    # Assert
    assert documento_str == "CPF: 123.456.789-01"


def test_criar_documento_outro_tipo_str():
    """Testa a representação string de um documento de outro tipo."""
    # Arrange
    documento = Documento(
        numero="123456789",
        tipo="RG"
    )

    # Act
    documento_str = str(documento)

    # Assert
    assert documento_str == "RG: 123456789" 