"""
Repositório de produtos.

Este módulo contém a interface do repositório de produtos
e suas implementações.
"""
from abc import abstractmethod
from typing import List, Optional

from ..entities.produto import Detalhe, Produto, Variacao
from .base import Repository


class ProdutoRepository(Repository[Produto]):
    """Interface do repositório de produtos."""

    @abstractmethod
    def buscar_por_codigo(self, codigo: str) -> Optional[Produto]:
        """
        Busca um produto pelo código.

        Args:
            codigo: Código do produto

        Returns:
            O produto encontrado ou None se não existir
        """
        pass

    @abstractmethod
    def buscar_por_nome(self, nome: str) -> List[Produto]:
        """
        Busca produtos pelo nome.

        Args:
            nome: Nome ou parte do nome do produto

        Returns:
            Lista de produtos encontrados
        """
        pass

    @abstractmethod
    def buscar_por_variacao(self, variacao_id: int) -> Optional[Produto]:
        """
        Busca um produto pela variação.

        Args:
            variacao_id: ID da variação

        Returns:
            O produto encontrado ou None se não existir
        """
        pass

    @abstractmethod
    def buscar_por_detalhe(self, tipo: str, valor: str) -> List[Produto]:
        """
        Busca produtos por um detalhe específico.

        Args:
            tipo: Tipo do detalhe
            valor: Valor do detalhe

        Returns:
            Lista de produtos encontrados
        """
        pass


class VariacaoRepository(Repository[Variacao]):
    """Interface do repositório de variações."""

    @abstractmethod
    def buscar_por_codigo(self, codigo: str) -> Optional[Variacao]:
        """
        Busca uma variação pelo código.

        Args:
            codigo: Código da variação

        Returns:
            A variação encontrada ou None se não existir
        """
        pass

    @abstractmethod
    def buscar_por_produto(self, produto_id: int) -> List[Variacao]:
        """
        Busca todas as variações de um produto.

        Args:
            produto_id: ID do produto

        Returns:
            Lista de variações do produto
        """
        pass


class DetalheRepository(Repository[Detalhe]):
    """Interface do repositório de detalhes."""

    @abstractmethod
    def buscar_por_tipo(self, tipo: str) -> List[Detalhe]:
        """
        Busca detalhes por tipo.

        Args:
            tipo: Tipo do detalhe

        Returns:
            Lista de detalhes do tipo especificado
        """
        pass

    @abstractmethod
    def buscar_por_produto(self, produto_id: int) -> List[Detalhe]:
        """
        Busca todos os detalhes de um produto.

        Args:
            produto_id: ID do produto

        Returns:
            Lista de detalhes do produto
        """
        pass

    @abstractmethod
    def buscar_por_variacao(self, variacao_id: int) -> List[Detalhe]:
        """
        Busca todos os detalhes de uma variação.

        Args:
            variacao_id: ID da variação

        Returns:
            Lista de detalhes da variação
        """
        pass
