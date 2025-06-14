"""
Testes para a entidade Fornecedor.

Este módulo contém os testes unitários para a entidade Fornecedor,
verificando se todas as validações e comportamentos funcionam conforme
esperado.
"""
import pytest

from src.joias.domain.catalogo.entities.fornecedor import Fornecedor, Documento
from src.joias.domain.shared.value_objects.endereco import Endereco


@pytest.fixture
def endereco_valido() -> Endereco:
    """Fixture que retorna um endereço válido para testes."""
    return Endereco(
        logradouro="Rua dos Testes",
        numero="123",
        bairro="Bairro Teste",
        cidade="Cidade Teste",
        estado="SP",
        cep="12345-678"
    )


@pytest.fixture
def documento_valido() -> Documento:
    """Fixture que retorna um documento válido para testes."""
    return Documento(
        numero="12345678901234",
        tipo="CNPJ"
    )


def test_criar_fornecedor_valido(endereco_valido, documento_valido):
    """Testa a criação de um fornecedor com dados válidos."""
    # Act
    fornecedor = Fornecedor(
        nome="Fornecedor Teste",
        documentos=[documento_valido],
        endereco=endereco_valido
    )

    # Assert
    assert fornecedor.nome == "Fornecedor Teste"
    assert len(fornecedor.documentos) == 1
    assert fornecedor.documentos[0].numero == "12345678901234"
    assert fornecedor.documentos[0].tipo == "CNPJ"
    assert fornecedor.endereco == endereco_valido
    assert fornecedor.ativo is True


def test_criar_fornecedor_sem_nome(endereco_valido, documento_valido):
    """Testa a tentativa de criar um fornecedor sem nome."""
    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        Fornecedor(
            nome="",
            documentos=[documento_valido],
            endereco=endereco_valido
        )
    assert "O nome não pode estar vazio" in str(exc_info.value)


def test_criar_fornecedor_sem_documentos(endereco_valido):
    """Testa a tentativa de criar um fornecedor sem documentos."""
    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        Fornecedor(
            nome="Fornecedor Teste",
            documentos=[],
            endereco=endereco_valido
        )
    assert "O fornecedor deve ter pelo menos um documento" in str(exc_info.value)


def test_adicionar_documento(endereco_valido, documento_valido):
    """Testa a adição de um novo documento ao fornecedor."""
    # Arrange
    fornecedor = Fornecedor(
        nome="Fornecedor Teste",
        documentos=[documento_valido],
        endereco=endereco_valido
    )
    novo_documento = Documento(
        numero="12345678901",
        tipo="CPF"
    )

    # Act
    fornecedor.adicionar_documento(novo_documento)

    # Assert
    assert len(fornecedor.documentos) == 2
    assert fornecedor.documentos[1].numero == "12345678901"
    assert fornecedor.documentos[1].tipo == "CPF"


def test_adicionar_documento_duplicado(endereco_valido, documento_valido):
    """Testa a tentativa de adicionar um documento duplicado."""
    # Arrange
    fornecedor = Fornecedor(
        nome="Fornecedor Teste",
        documentos=[documento_valido],
        endereco=endereco_valido
    )

    # Act
    fornecedor.adicionar_documento(documento_valido)

    # Assert
    assert len(fornecedor.documentos) == 1


def test_remover_documento(endereco_valido, documento_valido):
    """Testa a remoção de um documento do fornecedor."""
    # Arrange
    novo_documento = Documento(
        numero="12345678901",
        tipo="CPF"
    )
    fornecedor = Fornecedor(
        nome="Fornecedor Teste",
        documentos=[documento_valido, novo_documento],
        endereco=endereco_valido
    )

    # Act
    fornecedor.remover_documento(documento_valido)

    # Assert
    assert len(fornecedor.documentos) == 1
    assert fornecedor.documentos[0].numero == "12345678901"
    assert fornecedor.documentos[0].tipo == "CPF"


def test_remover_documento_unico(endereco_valido, documento_valido):
    """Testa a tentativa de remover o único documento do fornecedor."""
    # Arrange
    fornecedor = Fornecedor(
        nome="Fornecedor Teste",
        documentos=[documento_valido],
        endereco=endereco_valido
    )

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        fornecedor.remover_documento(documento_valido)
    assert "O fornecedor deve ter pelo menos um documento" in str(exc_info.value)


def test_atualizar_endereco(endereco_valido, documento_valido):
    """Testa a atualização do endereço do fornecedor."""
    # Arrange
    fornecedor = Fornecedor(
        nome="Fornecedor Teste",
        documentos=[documento_valido],
        endereco=endereco_valido
    )
    novo_endereco = Endereco(
        logradouro="Nova Rua",
        numero="456",
        bairro="Novo Bairro",
        cidade="Nova Cidade",
        estado="RJ",
        cep="98765-432"
    )

    # Act
    fornecedor.atualizar_endereco(novo_endereco)

    # Assert
    assert fornecedor.endereco == novo_endereco


def test_desativar_fornecedor(endereco_valido, documento_valido):
    """Testa a desativação do fornecedor."""
    # Arrange
    fornecedor = Fornecedor(
        nome="Fornecedor Teste",
        documentos=[documento_valido],
        endereco=endereco_valido
    )

    # Act
    fornecedor.desativar()

    # Assert
    assert fornecedor.ativo is False


def test_ativar_fornecedor(endereco_valido, documento_valido):
    """Testa a ativação do fornecedor."""
    # Arrange
    fornecedor = Fornecedor(
        nome="Fornecedor Teste",
        documentos=[documento_valido],
        endereco=endereco_valido
    )
    fornecedor.desativar()

    # Act
    fornecedor.ativar()

    # Assert
    assert fornecedor.ativo is True


def test_fornecedor_str(endereco_valido, documento_valido):
    """Testa a representação string do fornecedor."""
    # Arrange
    fornecedor = Fornecedor(
        nome="Fornecedor Teste",
        documentos=[documento_valido],
        endereco=endereco_valido
    )

    # Act
    fornecedor_str = str(fornecedor)

    # Assert
    assert fornecedor_str == (
        "Fornecedor Teste (ativo) - Documentos: [CNPJ: 12.345.678/0001-34]"
    ) 