"""
Repositório de pedidos.

Este módulo contém a interface do repositório de pedidos
e suas implementações.
"""
from abc import abstractmethod
from datetime import datetime
from typing import List, Optional

from ..entities.pedido import Pedido, StatusPedido
from .base import Repository


class PedidoRepository(Repository[Pedido]):
    """Interface do repositório de pedidos."""

    @abstractmethod
    def buscar_por_cliente(self, cliente_id: int) -> List[Pedido]:
        """
        Busca todos os pedidos de um cliente.

        Args:
            cliente_id: ID do cliente

        Returns:
            Lista de pedidos do cliente
        """
        pass

    @abstractmethod
    def buscar_por_status(self, status: StatusPedido) -> List[Pedido]:
        """
        Busca pedidos por status.

        Args:
            status: Status dos pedidos

        Returns:
            Lista de pedidos com o status especificado
        """
        pass

    @abstractmethod
    def buscar_por_periodo(
        self, data_inicio: datetime, data_fim: datetime
    ) -> List[Pedido]:
        """
        Busca pedidos em um período específico.

        Args:
            data_inicio: Data inicial do período
            data_fim: Data final do período

        Returns:
            Lista de pedidos no período especificado
        """
        pass

    @abstractmethod
    def buscar_por_produto(self, produto_id: int) -> List[Pedido]:
        """
        Busca pedidos que contêm um produto específico.

        Args:
            produto_id: ID do produto

        Returns:
            Lista de pedidos que contêm o produto
        """
        pass

    @abstractmethod
    def buscar_rascunhos_por_cliente(self, cliente_id: int) -> List[Pedido]:
        """
        Busca todos os pedidos em rascunho de um cliente.

        Args:
            cliente_id: ID do cliente

        Returns:
            Lista de pedidos em rascunho do cliente
        """
        pass

    @abstractmethod
    def buscar_pedidos_ativos(self) -> List[Pedido]:
        """
        Busca todos os pedidos ativos (não cancelados e não entregues).

        Returns:
            Lista de pedidos ativos
        """
        pass
