"""
Testes para o serviço de fornecedores.

Este módulo contém os testes unitários para o serviço de fornecedores,
verificando se todas as operações funcionam conforme esperado.
"""
import pytest
from unittest.mock import Mock, call

from src.joias.domain.catalogo.entities.fornecedor import Fornecedor, Documento
from src.joias.domain.catalogo.services.fornecedor_service import FornecedorService
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


@pytest.fixture
def fornecedor_valido(endereco_valido, documento_valido) -> Fornecedor:
    """Fixture que retorna um fornecedor válido para testes."""
    return Fornecedor(
        nome="Fornecedor Teste",
        documentos=[documento_valido],
        endereco=endereco_valido
    )


@pytest.fixture
def mock_repository():
    """Fixture que retorna um mock do repositório."""
    return Mock()


@pytest.fixture
def service(mock_repository):
    """Fixture que retorna o serviço de fornecedores com repositório mockado."""
    return FornecedorService(mock_repository)


def test_criar_fornecedor_com_sucesso(
    service,
    mock_repository,
    fornecedor_valido,
    documento_valido,
    endereco_valido
):
    """Testa a criação de um fornecedor com sucesso."""
    # Arrange
    mock_repository.buscar_por_documento.return_value = None
    mock_repository.salvar.return_value = fornecedor_valido

    # Act
    fornecedor = service.criar_fornecedor(
        nome="Fornecedor Teste",
        documento=documento_valido,
        endereco=endereco_valido
    )

    # Assert
    assert fornecedor.nome == "Fornecedor Teste"
    assert fornecedor.documentos[0].numero == documento_valido.numero
    assert fornecedor.documentos[0].tipo == documento_valido.tipo
    assert fornecedor.endereco == endereco_valido
    mock_repository.buscar_por_documento.assert_called_once_with(documento_valido)
    mock_repository.salvar.assert_called_once()


def test_criar_fornecedor_documento_duplicado(
    service,
    mock_repository,
    fornecedor_valido,
    documento_valido,
    endereco_valido
):
    """Testa a tentativa de criar um fornecedor com documento duplicado."""
    # Arrange
    mock_repository.buscar_por_documento.return_value = fornecedor_valido

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        service.criar_fornecedor(
            nome="Outro Fornecedor",
            documento=documento_valido,
            endereco=endereco_valido
        )
    assert "Já existe um fornecedor com o documento" in str(exc_info.value)
    mock_repository.salvar.assert_not_called()


def test_adicionar_documento_com_sucesso(
    service,
    mock_repository,
    fornecedor_valido
):
    """Testa a adição de um novo documento a um fornecedor."""
    # Arrange
    novo_documento = Documento(numero="12345678901", tipo="CPF")
    mock_repository.buscar_por_documento.return_value = None
    mock_repository.buscar_por_id.return_value = fornecedor_valido
    mock_repository.atualizar.return_value = fornecedor_valido

    # Act
    fornecedor = service.adicionar_documento(1, novo_documento)

    # Assert
    assert fornecedor is not None
    mock_repository.buscar_por_documento.assert_called_once_with(novo_documento)
    mock_repository.buscar_por_id.assert_called_once_with(1)
    mock_repository.atualizar.assert_called_once()


def test_remover_documento_com_sucesso(
    service,
    mock_repository,
    fornecedor_valido,
    documento_valido
):
    """Testa a remoção de um documento de um fornecedor."""
    # Arrange
    novo_documento = Documento(numero="12345678901", tipo="CPF")
    fornecedor_valido.adicionar_documento(novo_documento)
    mock_repository.buscar_por_id.return_value = fornecedor_valido
    mock_repository.atualizar.return_value = fornecedor_valido

    # Act
    fornecedor = service.remover_documento(1, documento_valido)

    # Assert
    assert fornecedor is not None
    assert len(fornecedor.documentos) == 1
    assert fornecedor.documentos[0].numero == novo_documento.numero
    mock_repository.buscar_por_id.assert_called_once_with(1)
    mock_repository.atualizar.assert_called_once()


def test_remover_documento_unico(
    service,
    mock_repository,
    fornecedor_valido,
    documento_valido
):
    """Testa a tentativa de remover o único documento de um fornecedor."""
    # Arrange
    mock_repository.buscar_por_id.return_value = fornecedor_valido

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        service.remover_documento(1, documento_valido)
    assert "O fornecedor deve ter pelo menos um documento" in str(exc_info.value)
    mock_repository.atualizar.assert_not_called()


def test_atualizar_endereco(
    service,
    mock_repository,
    fornecedor_valido
):
    """Testa a atualização do endereço de um fornecedor."""
    # Arrange
    novo_endereco = Endereco(
        logradouro="Nova Rua",
        numero="456",
        bairro="Novo Bairro",
        cidade="Nova Cidade",
        estado="RJ",
        cep="98765-432"
    )
    mock_repository.buscar_por_id.return_value = fornecedor_valido
    mock_repository.atualizar.return_value = fornecedor_valido

    # Act
    fornecedor = service.atualizar_endereco(1, novo_endereco)

    # Assert
    assert fornecedor is not None
    assert fornecedor.endereco == novo_endereco
    mock_repository.buscar_por_id.assert_called_once_with(1)
    mock_repository.atualizar.assert_called_once()


def test_buscar_por_nome(service, mock_repository, fornecedor_valido):
    """Testa a busca de fornecedores por nome."""
    # Arrange
    mock_repository.buscar_por_nome.return_value = [fornecedor_valido]

    # Act
    fornecedores = service.buscar_por_nome("Teste")

    # Assert
    assert len(fornecedores) == 1
    assert fornecedores[0].nome == "Fornecedor Teste"
    mock_repository.buscar_por_nome.assert_called_once_with("Teste")


def test_desativar_fornecedor(service, mock_repository, fornecedor_valido):
    """Testa a desativação de um fornecedor."""
    # Arrange
    mock_repository.buscar_por_id.return_value = fornecedor_valido
    mock_repository.atualizar.return_value = fornecedor_valido

    # Act
    resultado = service.desativar_fornecedor(1)

    # Assert
    assert resultado is True
    assert not fornecedor_valido.ativo
    mock_repository.buscar_por_id.assert_called_once_with(1)
    mock_repository.atualizar.assert_called_once()


def test_ativar_fornecedor(service, mock_repository, fornecedor_valido):
    """Testa a ativação de um fornecedor."""
    # Arrange
    fornecedor_valido.desativar()
    mock_repository.buscar_por_id.return_value = fornecedor_valido
    mock_repository.atualizar.return_value = fornecedor_valido

    # Act
    resultado = service.ativar_fornecedor(1)

    # Assert
    assert resultado is True
    assert fornecedor_valido.ativo
    mock_repository.buscar_por_id.assert_called_once_with(1)
    mock_repository.atualizar.assert_called_once() 