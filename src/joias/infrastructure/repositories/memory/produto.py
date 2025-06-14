"""
Repositório de produtos em memória.

Este módulo contém a implementação dos repositórios de produtos,
variações e detalhes em memória para testes.
"""
from typing import List, Optional

from ....domain.entities.produto import Detalhe, Produto, Variacao
from ....domain.repositories.produto import (
    DetalheRepository,
    ProdutoRepository,
    VariacaoRepository,
)
from .base import MemoryRepository


class MemoryProdutoRepository(MemoryRepository[Produto], ProdutoRepository):
    """
    Implementação do repositório de produtos em memória.

    Esta implementação é útil para testes e desenvolvimento.
    """

    def buscar_por_codigo(self, codigo: str) -> Optional[Produto]:
        """
        Busca um produto pelo código.

        Args:
            codigo: Código do produto

        Returns:
            O produto encontrado ou None se não existir
        """
        return next((p for p in self._items.values() if p.codigo == codigo), None)

    def buscar_por_nome(self, nome: str) -> List[Produto]:
        """
        Busca produtos pelo nome.

        Args:
            nome: Nome ou parte do nome do produto

        Returns:
            Lista de produtos encontrados
        """
        nome = nome.lower()
        return [p for p in self._items.values() if nome in p.nome.lower()]

    def buscar_por_variacao(self, variacao_id: int) -> Optional[Produto]:
        """
        Busca um produto pela variação.

        Args:
            variacao_id: ID da variação

        Returns:
            O produto encontrado ou None se não existir
        """
        return next(
            (
                p
                for p in self._items.values()
                for v in p.variacoes
                if v.id == variacao_id
            ),
            None,
        )

    def buscar_por_detalhe(self, tipo: str, valor: str) -> List[Produto]:
        """
        Busca produtos por um detalhe específico.

        Args:
            tipo: Tipo do detalhe
            valor: Valor do detalhe

        Returns:
            Lista de produtos encontrados
        """
        return [
            p
            for p in self._items.values()
            if any(d.tipo == tipo and d.valor == valor for d in p.detalhes)
        ]


class MemoryVariacaoRepository(MemoryRepository[Variacao], VariacaoRepository):
    """
    Implementação do repositório de variações em memória.

    Esta implementação é útil para testes e desenvolvimento.
    """

    def buscar_por_codigo(self, codigo: str) -> Optional[Variacao]:
        """
        Busca uma variação pelo código.

        Args:
            codigo: Código da variação

        Returns:
            A variação encontrada ou None se não existir
        """
        return next((v for v in self._items.values() if v.codigo == codigo), None)

    def buscar_por_produto(self, produto_id: int) -> List[Variacao]:
        """
        Busca todas as variações de um produto.

        Args:
            produto_id: ID do produto

        Returns:
            Lista de variações do produto
        """
        # Na implementação em memória, as variações são armazenadas
        # diretamente no produto, então este método não é usado
        return []


class MemoryDetalheRepository(MemoryRepository[Detalhe], DetalheRepository):
    """
    Implementação do repositório de detalhes em memória.

    Esta implementação é útil para testes e desenvolvimento.
    """

    def buscar_por_tipo(self, tipo: str) -> List[Detalhe]:
        """
        Busca detalhes por tipo.

        Args:
            tipo: Tipo do detalhe

        Returns:
            Lista de detalhes do tipo especificado
        """
        return [d for d in self._items.values() if d.tipo == tipo]

    def buscar_por_produto(self, produto_id: int) -> List[Detalhe]:
        """
        Busca todos os detalhes de um produto.

        Args:
            produto_id: ID do produto

        Returns:
            Lista de detalhes do produto
        """
        # Na implementação em memória, os detalhes são armazenados
        # diretamente no produto, então este método não é usado
        return []

    def buscar_por_variacao(self, variacao_id: int) -> List[Detalhe]:
        """
        Busca todos os detalhes de uma variação.

        Args:
            variacao_id: ID da variação

        Returns:
            Lista de detalhes da variação
        """
        # Na implementação em memória, os detalhes são armazenados
        # diretamente na variação, então este método não é usado
        return []
