"""
Repositório de pedidos em memória.

Este módulo contém a implementação do repositório de pedidos
em memória para testes.
"""
from datetime import datetime
from typing import List

from ....domain.entities.pedido import Pedido, StatusPedido
from ....domain.repositories.pedido import PedidoRepository
from .base import MemoryRepository


class MemoryPedidoRepository(MemoryRepository[Pedido], PedidoRepository):
    """
    Implementação do repositório de pedidos em memória.

    Esta implementação é útil para testes e desenvolvimento.
    """

    def buscar_por_cliente(self, cliente_id: int) -> List[Pedido]:
        """
        Busca todos os pedidos de um cliente.

        Args:
            cliente_id: ID do cliente

        Returns:
            Lista de pedidos do cliente
        """
        return [p for p in self._items.values() if p.cliente.id == cliente_id]

    def buscar_por_status(self, status: StatusPedido) -> List[Pedido]:
        """
        Busca pedidos por status.

        Args:
            status: Status dos pedidos

        Returns:
            Lista de pedidos com o status especificado
        """
        return [p for p in self._items.values() if p.status == status]

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
        return [
            p for p in self._items.values() if data_inicio <= p.data_criacao <= data_fim
        ]

    def buscar_por_produto(self, produto_id: int) -> List[Pedido]:
        """
        Busca pedidos que contêm um produto específico.

        Args:
            produto_id: ID do produto

        Returns:
            Lista de pedidos que contêm o produto
        """
        return [
            p
            for p in self._items.values()
            if any(i.produto.id == produto_id for i in p.itens)
        ]

    def buscar_rascunhos_por_cliente(self, cliente_id: int) -> List[Pedido]:
        """
        Busca todos os pedidos em rascunho de um cliente.

        Args:
            cliente_id: ID do cliente

        Returns:
            Lista de pedidos em rascunho do cliente
        """
        return [
            p
            for p in self._items.values()
            if p.cliente.id == cliente_id and p.status == StatusPedido.RASCUNHO
        ]

    def buscar_pedidos_ativos(self) -> List[Pedido]:
        """
        Busca todos os pedidos ativos (não cancelados e não entregues).

        Returns:
            Lista de pedidos ativos
        """
        status_inativos = {StatusPedido.CANCELADO, StatusPedido.ENTREGUE}
        return [p for p in self._items.values() if p.status not in status_inativos]
