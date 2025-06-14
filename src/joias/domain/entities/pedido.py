"""
Entidades relacionadas a pedidos.

Este módulo contém as entidades que representam pedidos,
seus itens e status.
"""
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional

from .base import Entity
from .dados_pessoais import Endereco
from .produto import Produto, Variacao
from .usuario import Usuario


class StatusPedido(Enum):
    """Enumeração dos possíveis status de um pedido."""

    RASCUNHO = "rascunho"
    AGUARDANDO_PAGAMENTO = "aguardando_pagamento"
    PAGO = "pago"
    EM_PRODUCAO = "em_producao"
    PRONTO_PARA_ENVIO = "pronto_para_envio"
    ENVIADO = "enviado"
    ENTREGUE = "entregue"
    CANCELADO = "cancelado"


@dataclass
class ItemPedido(Entity):
    """
    Entidade que representa um item de pedido.

    Um item de pedido é um produto específico com sua
    quantidade e preço no momento da compra.
    """

    produto: Produto
    quantidade: int
    preco_unitario: Decimal
    variacao: Optional[Variacao] = None
    desconto: Decimal = Decimal("0")

    @property
    def subtotal(self) -> Decimal:
        """
        Calcula o subtotal do item (preço * quantidade - desconto).

        Returns:
            Valor total do item com desconto
        """
        return (self.preco_unitario * self.quantidade) - self.desconto


@dataclass
class Pedido(Entity):
    """
    Entidade que representa um pedido.

    Um pedido é uma solicitação de compra feita por um cliente,
    contendo um ou mais itens.
    """

    cliente: Usuario
    status: StatusPedido = StatusPedido.RASCUNHO
    data_criacao: datetime = field(default_factory=datetime.now)
    data_modificacao: datetime = field(default_factory=datetime.now)
    itens: List[ItemPedido] = field(default_factory=list)
    endereco_entrega: Optional[Endereco] = None
    desconto_total: Decimal = Decimal("0")
    observacoes: Optional[str] = None

    def adicionar_item(self, item: ItemPedido) -> None:
        """
        Adiciona um item ao pedido.

        Args:
            item: Item a ser adicionado
        """
        self.itens.append(item)
        self.atualizar()

    def remover_item(self, item_id: int) -> None:
        """
        Remove um item do pedido.

        Args:
            item_id: ID do item a ser removido
        """
        self.itens = [i for i in self.itens if i.id != item_id]
        self.atualizar()

    def atualizar_status(self, novo_status: StatusPedido) -> None:
        """
        Atualiza o status do pedido.

        Args:
            novo_status: Novo status do pedido
        """
        self.status = novo_status
        self.data_modificacao = datetime.now()
        self.atualizar()

    def definir_endereco_entrega(self, endereco: Endereco) -> None:
        """
        Define o endereço de entrega do pedido.

        Args:
            endereco: Endereço de entrega
        """
        self.endereco_entrega = endereco
        self.atualizar()

    @property
    def subtotal(self) -> Decimal:
        """
        Calcula o subtotal do pedido (soma dos subtotais dos itens).

        Returns:
            Valor total dos itens
        """
        return sum(item.subtotal for item in self.itens)

    @property
    def total(self) -> Decimal:
        """
        Calcula o total do pedido (subtotal - desconto total).

        Returns:
            Valor total do pedido com desconto
        """
        return self.subtotal - self.desconto_total

    def pode_modificar(self) -> bool:
        """
        Verifica se o pedido pode ser modificado.

        Returns:
            True se o pedido pode ser modificado, False caso contrário
        """
        return self.status in [StatusPedido.RASCUNHO, StatusPedido.AGUARDANDO_PAGAMENTO]
