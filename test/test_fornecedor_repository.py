"""
Testes para o repositório SQLAlchemy de fornecedores.

Este módulo contém os testes de integração para o repositório SQLAlchemy
de fornecedores, verificando se todas as operações com o banco de dados
funcionam conforme esperado.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.joias.domain.catalogo.entities.fornecedor import Fornecedor, Documento
from src.joias.domain.shared.value_objects.endereco import Endereco
from src.joias.infrastructure.persistence.sqlalchemy.models.base import Base
from src.joias.infrastructure.persistence.sqlalchemy.repositories.fornecedor_repository import (
    SQLAlchemyFornecedorRepository
)


@pytest.fixture(scope="session")
def engine():
    """Fixture que cria o engine SQLAlchemy para testes."""
    return create_engine("sqlite:///:memory:")


@pytest.fixture(scope="session")
def tables(engine):
    """Fixture que cria as tabelas no banco de dados de teste."""
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def session(engine, tables):
    """
    Fixture que cria uma sessão SQLAlchemy para testes.

    A sessão é criada dentro de uma transação que é revertida ao final
    de cada teste, garantindo o isolamento entre os testes.
    """
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def repository(session):
    """Fixture que retorna o repositório SQLAlchemy para testes."""
    return SQLAlchemyFornecedorRepository(session)


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


def test_salvar_fornecedor(repository, fornecedor_valido):
    """Testa a persistência de um fornecedor no banco de dados."""
    # Act
    fornecedor = repository.salvar(fornecedor_valido)

    # Assert
    assert fornecedor is not None
    assert fornecedor.nome == "Fornecedor Teste"
    assert len(fornecedor.documentos) == 1
    assert fornecedor.documentos[0].numero == "12345678901234"
    assert fornecedor.documentos[0].tipo == "CNPJ"
    assert fornecedor.endereco.logradouro == "Rua dos Testes"
    assert fornecedor.endereco.numero == "123"
    assert fornecedor.endereco.bairro == "Bairro Teste"
    assert fornecedor.endereco.cidade == "Cidade Teste"
    assert fornecedor.endereco.estado == "SP"
    assert fornecedor.endereco.cep == "12345-678"


def test_buscar_por_id(repository, fornecedor_valido):
    """Testa a busca de um fornecedor por ID."""
    # Arrange
    fornecedor_salvo = repository.salvar(fornecedor_valido)

    # Act
    fornecedor = repository.buscar_por_id(fornecedor_salvo.id)

    # Assert
    assert fornecedor is not None
    assert fornecedor.nome == "Fornecedor Teste"
    assert len(fornecedor.documentos) == 1
    assert fornecedor.documentos[0].numero == "12345678901234"


def test_buscar_por_documento(repository, fornecedor_valido, documento_valido):
    """Testa a busca de um fornecedor por documento."""
    # Arrange
    repository.salvar(fornecedor_valido)

    # Act
    fornecedor = repository.buscar_por_documento(documento_valido)

    # Assert
    assert fornecedor is not None
    assert fornecedor.nome == "Fornecedor Teste"
    assert len(fornecedor.documentos) == 1
    assert fornecedor.documentos[0].numero == "12345678901234"


def test_listar_fornecedores(repository, fornecedor_valido):
    """Testa a listagem de fornecedores."""
    # Arrange
    repository.salvar(fornecedor_valido)

    # Act
    fornecedores = repository.listar()

    # Assert
    assert len(fornecedores) == 1
    assert fornecedores[0].nome == "Fornecedor Teste"


def test_listar_fornecedores_apenas_ativos(repository, fornecedor_valido):
    """Testa a listagem de fornecedores ativos."""
    # Arrange
    fornecedor_valido.desativar()
    repository.salvar(fornecedor_valido)

    # Act
    fornecedores = repository.listar(apenas_ativos=True)

    # Assert
    assert len(fornecedores) == 0


def test_buscar_por_nome(repository, fornecedor_valido):
    """Testa a busca de fornecedores por nome."""
    # Arrange
    repository.salvar(fornecedor_valido)

    # Act
    fornecedores = repository.buscar_por_nome("Teste")

    # Assert
    assert len(fornecedores) == 1
    assert fornecedores[0].nome == "Fornecedor Teste"


def test_atualizar_fornecedor(repository, fornecedor_valido):
    """Testa a atualização de um fornecedor."""
    # Arrange
    fornecedor_salvo = repository.salvar(fornecedor_valido)
    fornecedor_salvo.nome = "Novo Nome"

    # Act
    fornecedor = repository.atualizar(fornecedor_salvo)

    # Assert
    assert fornecedor is not None
    assert fornecedor.nome == "Novo Nome"


def test_excluir_fornecedor(repository, fornecedor_valido):
    """Testa a exclusão de um fornecedor."""
    # Arrange
    fornecedor_salvo = repository.salvar(fornecedor_valido)

    # Act
    resultado = repository.excluir(fornecedor_salvo.id)
    fornecedor = repository.buscar_por_id(fornecedor_salvo.id)

    # Assert
    assert resultado is True
    assert fornecedor is None 