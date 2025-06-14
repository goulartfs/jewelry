"""
Testes para o serviço de aplicação de fornecedores.

Este módulo contém os testes unitários para o serviço de aplicação
de fornecedores, verificando se todas as operações funcionam conforme
esperado.
"""
import pytest
from unittest.mock import Mock, call

from src.joias.domain.catalogo.entities.fornecedor import Fornecedor, Documento
from src.joias.domain.shared.value_objects.endereco import Endereco
from src.joias.application.catalogo.services.fornecedor_app_service import (
    FornecedorAppService
)
from src.joias.application.catalogo.dtos.fornecedor_dto import (
    FornecedorDTO,
    CriarFornecedorDTO,
    AtualizarFornecedorDTO,
    ListagemFornecedorDTO,
    DocumentoDTO,
    EnderecoDTO
)


@pytest.fixture
def endereco_dto() -> EnderecoDTO:
    """Fixture que retorna um DTO de endereço válido para testes."""
    return EnderecoDTO(
        logradouro="Rua dos Testes",
        numero="123",
        bairro="Bairro Teste",
        cidade="Cidade Teste",
        estado="SP",
        cep="12345-678"
    )


@pytest.fixture
def endereco_valido(endereco_dto) -> Endereco:
    """Fixture que retorna um endereço válido para testes."""
    return Endereco(
        logradouro=endereco_dto.logradouro,
        numero=endereco_dto.numero,
        bairro=endereco_dto.bairro,
        cidade=endereco_dto.cidade,
        estado=endereco_dto.estado,
        cep=endereco_dto.cep
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
    """Fixture que retorna o serviço de aplicação com repositório mockado."""
    return FornecedorAppService(mock_repository)


def test_criar_fornecedor(
    service,
    mock_repository,
    fornecedor_valido,
    endereco_dto
):
    """Testa a criação de um fornecedor."""
    # Arrange
    mock_repository.buscar_por_documento.return_value = None
    mock_repository.salvar.return_value = fornecedor_valido

    dto = CriarFornecedorDTO(
        nome="Fornecedor Teste",
        documento_numero="12345678901234",
        documento_tipo="CNPJ",
        endereco=endereco_dto
    )

    # Act
    fornecedor = service.criar_fornecedor(dto)

    # Assert
    assert fornecedor is not None
    assert fornecedor.nome == "Fornecedor Teste"
    assert len(fornecedor.documentos) == 1
    assert fornecedor.documentos[0].numero == "12345678901234"
    assert fornecedor.documentos[0].tipo == "CNPJ"
    mock_repository.buscar_por_documento.assert_called_once()
    mock_repository.salvar.assert_called_once()


def test_atualizar_fornecedor(
    service,
    mock_repository,
    fornecedor_valido,
    endereco_dto
):
    """Testa a atualização de um fornecedor."""
    # Arrange
    mock_repository.buscar_por_id.return_value = fornecedor_valido
    mock_repository.atualizar.return_value = fornecedor_valido

    dto = AtualizarFornecedorDTO(
        nome="Novo Nome",
        endereco=endereco_dto
    )

    # Act
    fornecedor = service.atualizar_fornecedor(1, dto)

    # Assert
    assert fornecedor is not None
    assert fornecedor.nome == "Novo Nome"
    mock_repository.buscar_por_id.assert_called_once_with(1)
    mock_repository.atualizar.assert_called_once()


def test_buscar_por_id(service, mock_repository, fornecedor_valido):
    """Testa a busca de um fornecedor por ID."""
    # Arrange
    mock_repository.buscar_por_id.return_value = fornecedor_valido

    # Act
    fornecedor = service.buscar_por_id(1)

    # Assert
    assert fornecedor is not None
    assert fornecedor.nome == "Fornecedor Teste"
    mock_repository.buscar_por_id.assert_called_once_with(1)


def test_listar_fornecedores(service, mock_repository, fornecedor_valido):
    """Testa a listagem de fornecedores."""
    # Arrange
    mock_repository.listar.return_value = [fornecedor_valido]

    # Act
    fornecedores = service.listar()

    # Assert
    assert len(fornecedores) == 1
    assert fornecedores[0].nome == "Fornecedor Teste"
    assert fornecedores[0].cidade == "Cidade Teste"
    assert fornecedores[0].estado == "SP"
    mock_repository.listar.assert_called_once_with(True)


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
    mock_repository.buscar_por_id.assert_called_once_with(1)
    mock_repository.atualizar.assert_called_once() 