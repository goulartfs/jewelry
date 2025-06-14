"""
Casos de uso relacionados a produtos.

Este módulo contém os casos de uso para operações
relacionadas a produtos.
"""
from dataclasses import dataclass
from decimal import Decimal
from typing import List, Optional

from ...domain.entities.produto import Detalhe, Preco, Produto, Variacao
from ...domain.repositories.produto import (
    DetalheRepository,
    ProdutoRepository,
    VariacaoRepository,
)
from .base import UseCase


@dataclass
class CriarProdutoInput:
    """Dados de entrada para criação de produto."""

    nome: str
    descricao: str
    codigo: str
    preco: Decimal
    detalhes: Optional[List[Detalhe]] = None
    variacoes: Optional[List[Variacao]] = None


class CriarProdutoUseCase(UseCase[CriarProdutoInput, Produto]):
    """Caso de uso para criar um novo produto."""

    def __init__(self, produto_repository: ProdutoRepository):
        self.produto_repository = produto_repository

    def execute(self, input_data: CriarProdutoInput) -> Produto:
        """
        Executa o caso de uso.

        Args:
            input_data: Dados de entrada

        Returns:
            Produto criado

        Raises:
            ValueError: Se o código já existir
        """
        if self.produto_repository.buscar_por_codigo(input_data.codigo):
            raise ValueError("Código já existe")

        produto = Produto(
            nome=input_data.nome,
            descricao=input_data.descricao,
            codigo=input_data.codigo,
            preco=Preco(valor=input_data.preco),
            detalhes=input_data.detalhes or [],
            variacoes=input_data.variacoes or [],
        )

        return self.produto_repository.criar(produto)


@dataclass
class AtualizarProdutoInput:
    """Dados de entrada para atualização de produto."""

    id: int
    nome: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[Decimal] = None


class AtualizarProdutoUseCase(UseCase[AtualizarProdutoInput, Produto]):
    """Caso de uso para atualizar um produto existente."""

    def __init__(self, produto_repository: ProdutoRepository):
        self.produto_repository = produto_repository

    def execute(self, input_data: AtualizarProdutoInput) -> Produto:
        """
        Executa o caso de uso.

        Args:
            input_data: Dados de entrada

        Returns:
            Produto atualizado

        Raises:
            ValueError: Se o produto não existir
        """
        produto = self.produto_repository.buscar_por_id(input_data.id)
        if not produto:
            raise ValueError("Produto não encontrado")

        if input_data.nome:
            produto.nome = input_data.nome
        if input_data.descricao:
            produto.descricao = input_data.descricao
        if input_data.preco:
            produto.atualizar_preco(Preco(valor=input_data.preco))

        return self.produto_repository.atualizar(produto)


class DeletarProdutoUseCase(UseCase[int, None]):
    """Caso de uso para deletar um produto."""

    def __init__(self, produto_repository: ProdutoRepository):
        self.produto_repository = produto_repository

    def execute(self, produto_id: int) -> None:
        """
        Executa o caso de uso.

        Args:
            produto_id: ID do produto a ser deletado

        Raises:
            ValueError: Se o produto não existir
        """
        produto = self.produto_repository.buscar_por_id(produto_id)
        if not produto:
            raise ValueError("Produto não encontrado")

        self.produto_repository.deletar(produto)


@dataclass
class AdicionarVariacaoInput:
    """Dados de entrada para adicionar variação a um produto."""

    produto_id: int
    nome: str
    descricao: str
    codigo: str
    detalhes: Optional[List[Detalhe]] = None


class AdicionarVariacaoUseCase(UseCase[AdicionarVariacaoInput, Produto]):
    """Caso de uso para adicionar uma variação a um produto."""

    def __init__(
        self,
        produto_repository: ProdutoRepository,
        variacao_repository: VariacaoRepository,
    ):
        self.produto_repository = produto_repository
        self.variacao_repository = variacao_repository

    def execute(self, input_data: AdicionarVariacaoInput) -> Produto:
        """
        Executa o caso de uso.

        Args:
            input_data: Dados de entrada

        Returns:
            Produto com a nova variação

        Raises:
            ValueError: Se o produto não existir ou se o código já existir
        """
        produto = self.produto_repository.buscar_por_id(input_data.produto_id)
        if not produto:
            raise ValueError("Produto não encontrado")

        if self.variacao_repository.buscar_por_codigo(input_data.codigo):
            raise ValueError("Código de variação já existe")

        variacao = Variacao(
            nome=input_data.nome,
            descricao=input_data.descricao,
            codigo=input_data.codigo,
            detalhes=input_data.detalhes or [],
        )

        produto.adicionar_variacao(variacao)
        return self.produto_repository.atualizar(produto)


@dataclass
class AdicionarDetalheInput:
    """Dados de entrada para adicionar detalhe a um produto."""

    produto_id: int
    nome: str
    valor: str
    tipo: str


class AdicionarDetalheUseCase(UseCase[AdicionarDetalheInput, Produto]):
    """Caso de uso para adicionar um detalhe a um produto."""

    def __init__(self, produto_repository: ProdutoRepository):
        self.produto_repository = produto_repository

    def execute(self, input_data: AdicionarDetalheInput) -> Produto:
        """
        Executa o caso de uso.

        Args:
            input_data: Dados de entrada

        Returns:
            Produto com o novo detalhe

        Raises:
            ValueError: Se o produto não existir
        """
        produto = self.produto_repository.buscar_por_id(input_data.produto_id)
        if not produto:
            raise ValueError("Produto não encontrado")

        detalhe = Detalhe(
            nome=input_data.nome, valor=input_data.valor, tipo=input_data.tipo
        )

        produto.adicionar_detalhe(detalhe)
        return self.produto_repository.atualizar(produto)


class BuscarProdutosUseCase(UseCase[str, List[Produto]]):
    """Caso de uso para buscar produtos por nome."""

    def __init__(self, produto_repository: ProdutoRepository):
        self.produto_repository = produto_repository

    def execute(self, nome: str) -> List[Produto]:
        """
        Executa o caso de uso.

        Args:
            nome: Nome ou parte do nome do produto

        Returns:
            Lista de produtos encontrados
        """
        return self.produto_repository.buscar_por_nome(nome)
