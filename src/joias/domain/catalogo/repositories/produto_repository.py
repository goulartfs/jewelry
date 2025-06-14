"""
Interface do repositório de produtos.

Este módulo define a interface que deve ser implementada por qualquer
repositório que queira persistir produtos.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from decimal import Decimal

from ..entities.produto import Produto


class ProdutoRepository(ABC):
    """
    Interface para repositório de produtos.

    Esta é uma interface que define os métodos que devem ser implementados
    por qualquer repositório que queira persistir produtos, seguindo o
    princípio de inversão de dependência do SOLID.
    """

    @abstractmethod
    def salvar(self, produto: Produto) -> Produto:
        """
        Salva um produto no repositório.

        Args:
            produto: O produto a ser salvo

        Returns:
            Produto: O produto salvo com ID atualizado
        """
        pass

    @abstractmethod
    def buscar_por_id(self, produto_id: int) -> Optional[Produto]:
        """
        Busca um produto pelo ID.

        Args:
            produto_id: ID do produto

        Returns:
            Optional[Produto]: O produto encontrado ou None
        """
        pass

    @abstractmethod
    def buscar_por_sku(self, sku: str) -> Optional[Produto]:
        """
        Busca um produto pelo SKU.

        Args:
            sku: SKU do produto

        Returns:
            Optional[Produto]: O produto encontrado ou None
        """
        pass

    @abstractmethod
    def listar(self, apenas_ativos: bool = True) -> List[Produto]:
        """
        Lista todos os produtos.

        Args:
            apenas_ativos: Se True, retorna apenas produtos ativos

        Returns:
            List[Produto]: Lista de produtos
        """
        pass

    @abstractmethod
    def buscar_por_faixa_de_preco(
        self,
        preco_minimo: Decimal,
        preco_maximo: Decimal
    ) -> List[Produto]:
        """
        Busca produtos por faixa de preço.

        Args:
            preco_minimo: Preço mínimo
            preco_maximo: Preço máximo

        Returns:
            List[Produto]: Lista de produtos na faixa de preço
        """
        pass

    @abstractmethod
    def atualizar(self, produto: Produto) -> Optional[Produto]:
        """
        Atualiza um produto existente.

        Args:
            produto: O produto com dados atualizados

        Returns:
            Optional[Produto]: O produto atualizado ou None se não encontrado
        """
        pass

    @abstractmethod
    def excluir(self, produto_id: int) -> bool:
        """
        Remove um produto.

        Args:
            produto_id: ID do produto

        Returns:
            bool: True se removido com sucesso, False caso contrário
        """
        pass 