"""
Testes para o objeto de valor Endereco.

Este módulo contém os testes unitários para o objeto de valor Endereco,
verificando se todas as validações e comportamentos funcionam conforme
esperado.
"""
import pytest

from src.joias.domain.shared.value_objects.endereco import Endereco


def test_criar_endereco_valido():
    """Testa a criação de um endereço com dados válidos."""
    # Act
    endereco = Endereco(
        logradouro="Rua dos Testes",
        numero="123",
        bairro="Bairro Teste",
        cidade="Cidade Teste",
        estado="SP",
        cep="12345-678"
    )

    # Assert
    assert endereco.logradouro == "Rua dos Testes"
    assert endereco.numero == "123"
    assert endereco.bairro == "Bairro Teste"
    assert endereco.cidade == "Cidade Teste"
    assert endereco.estado == "SP"
    assert endereco.cep == "12345-678"
    assert endereco.complemento is None
    assert endereco.pais == "Brasil"


def test_criar_endereco_com_complemento():
    """Testa a criação de um endereço com complemento."""
    # Act
    endereco = Endereco(
        logradouro="Rua dos Testes",
        numero="123",
        bairro="Bairro Teste",
        cidade="Cidade Teste",
        estado="SP",
        cep="12345-678",
        complemento="Apto 101"
    )

    # Assert
    assert endereco.complemento == "Apto 101"


def test_criar_endereco_com_pais_diferente():
    """Testa a criação de um endereço com país diferente do padrão."""
    # Act
    endereco = Endereco(
        logradouro="Test Street",
        numero="123",
        bairro="Test District",
        cidade="Test City",
        estado="CA",
        cep="12345",
        pais="Estados Unidos"
    )

    # Assert
    assert endereco.pais == "Estados Unidos"


def test_criar_endereco_sem_logradouro():
    """Testa a tentativa de criar um endereço sem logradouro."""
    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        Endereco(
            logradouro="",
            numero="123",
            bairro="Bairro Teste",
            cidade="Cidade Teste",
            estado="SP",
            cep="12345-678"
        )
    assert "O logradouro não pode estar vazio" in str(exc_info.value)


def test_criar_endereco_sem_numero():
    """Testa a tentativa de criar um endereço sem número."""
    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        Endereco(
            logradouro="Rua dos Testes",
            numero="",
            bairro="Bairro Teste",
            cidade="Cidade Teste",
            estado="SP",
            cep="12345-678"
        )
    assert "O número não pode estar vazio" in str(exc_info.value)


def test_criar_endereco_sem_bairro():
    """Testa a tentativa de criar um endereço sem bairro."""
    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        Endereco(
            logradouro="Rua dos Testes",
            numero="123",
            bairro="",
            cidade="Cidade Teste",
            estado="SP",
            cep="12345-678"
        )
    assert "O bairro não pode estar vazio" in str(exc_info.value)


def test_criar_endereco_sem_cidade():
    """Testa a tentativa de criar um endereço sem cidade."""
    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        Endereco(
            logradouro="Rua dos Testes",
            numero="123",
            bairro="Bairro Teste",
            cidade="",
            estado="SP",
            cep="12345-678"
        )
    assert "A cidade não pode estar vazia" in str(exc_info.value)


def test_criar_endereco_sem_estado():
    """Testa a tentativa de criar um endereço sem estado."""
    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        Endereco(
            logradouro="Rua dos Testes",
            numero="123",
            bairro="Bairro Teste",
            cidade="Cidade Teste",
            estado="",
            cep="12345-678"
        )
    assert "O estado não pode estar vazio" in str(exc_info.value)


def test_criar_endereco_sem_cep():
    """Testa a tentativa de criar um endereço sem CEP."""
    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        Endereco(
            logradouro="Rua dos Testes",
            numero="123",
            bairro="Bairro Teste",
            cidade="Cidade Teste",
            estado="SP",
            cep=""
        )
    assert "O CEP não pode estar vazio" in str(exc_info.value)


def test_criar_endereco_cep_invalido():
    """Testa a tentativa de criar um endereço com CEP inválido."""
    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        Endereco(
            logradouro="Rua dos Testes",
            numero="123",
            bairro="Bairro Teste",
            cidade="Cidade Teste",
            estado="SP",
            cep="123"
        )
    assert "O CEP deve ter 8 dígitos" in str(exc_info.value)


def test_criar_endereco_estado_maiusculo():
    """Testa se o estado é convertido para maiúsculas."""
    # Act
    endereco = Endereco(
        logradouro="Rua dos Testes",
        numero="123",
        bairro="Bairro Teste",
        cidade="Cidade Teste",
        estado="sp",
        cep="12345-678"
    )

    # Assert
    assert endereco.estado == "SP"


def test_criar_endereco_cep_formatado():
    """Testa se o CEP é formatado corretamente."""
    # Act
    endereco = Endereco(
        logradouro="Rua dos Testes",
        numero="123",
        bairro="Bairro Teste",
        cidade="Cidade Teste",
        estado="SP",
        cep="12345678"
    )

    # Assert
    assert endereco.cep == "12345-678"


def test_criar_endereco_cep_com_mascara():
    """Testa se o CEP com máscara é aceito e formatado corretamente."""
    # Act
    endereco = Endereco(
        logradouro="Rua dos Testes",
        numero="123",
        bairro="Bairro Teste",
        cidade="Cidade Teste",
        estado="SP",
        cep="12.345-678"
    )

    # Assert
    assert endereco.cep == "12345-678"


def test_endereco_str():
    """Testa a representação string do endereço."""
    # Arrange
    endereco = Endereco(
        logradouro="Rua dos Testes",
        numero="123",
        bairro="Bairro Teste",
        cidade="Cidade Teste",
        estado="SP",
        cep="12345-678",
        complemento="Apto 101"
    )

    # Act
    endereco_str = str(endereco)

    # Assert
    assert endereco_str == (
        "Rua dos Testes, 123, Apto 101, Bairro Teste, "
        "Cidade Teste/SP, 12345-678"
    ) 