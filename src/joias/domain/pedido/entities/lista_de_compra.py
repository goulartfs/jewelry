"""
Entidade que representa uma lista de compras.

Este módulo define a estrutura e comportamento de uma lista de compras,
que pode ser posteriormente convertida em um pedido.
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime
from uuid import UUID, uuid4
from decimal import Decimal

from .item import Item
from ...shared.value_objects.preco import Preco


@dataclass
class ListaDeCompra:
    """
    Representa uma lista de compras que pode ser convertida em um pedido.

    Esta é uma entidade que encapsula uma coleção de itens e suas informações
    relacionadas, permitindo o gerenciamento de uma lista de compras antes
    de sua conversão em um pedido efetivo.

    Attributes:
        nome: Nome/título da lista
        items: Lista de itens
        id: Identificador único da lista
        data_criacao: Data de criação da lista
        data_atualizacao: Data da última atualização
        notas: Observações gerais sobre a lista
    """
    nome: str
    items: List[Item] = field(default_factory=list)
    id: UUID = field(default_factory=uuid4)
    data_criacao: datetime = field(default_factory=datetime.now)
    data_atualizacao: datetime = field(default_factory=datetime.now)
    notas: Optional[str] = None

    def adicionar_item(self, item: Item) -> None:
        """
        Adiciona um item à lista.

        Args:
            item: O item a ser adicionado
        """
        self.items.append(item)
        self._atualizar()

    def remover_item(self, item: Item) -> None:
        """
        Remove um item da lista.

        Args:
            item: O item a ser removido

        Raises:
            ValueError: Se o item não estiver na lista
        """
        if item not in self.items:
            raise ValueError("Item não encontrado na lista")
        
        self.items.remove(item)
        self._atualizar()

    def atualizar_quantidade(self, item: Item, nova_quantidade: int) -> None:
        """
        Atualiza a quantidade de um item na lista.

        Args:
            item: O item a ser atualizado
            nova_quantidade: A nova quantidade

        Raises:
            ValueError: Se o item não estiver na lista ou se a quantidade for inválida
        """
        if item not in self.items:
            raise ValueError("Item não encontrado na lista")
        
        if nova_quantidade <= 0:
            self.remover_item(item)
        else:
            idx = self.items.index(item)
            self.items[idx].atualizar_quantidade(nova_quantidade)
            self._atualizar()

    def aplicar_desconto_item(self, item: Item, percentual: Decimal) -> None:
        """
        Aplica um desconto a um item específico.

        Args:
            item: O item a receber o desconto
            percentual: Percentual de desconto (0-100)

        Raises:
            ValueError: Se o item não estiver na lista
        """
        if item not in self.items:
            raise ValueError("Item não encontrado na lista")
        
        idx = self.items.index(item)
        self.items[idx].aplicar_desconto(percentual)
        self._atualizar()

    def remover_desconto_item(self, item: Item) -> None:
        """
        Remove o desconto de um item específico.

        Args:
            item: O item a ter o desconto removido

        Raises:
            ValueError: Se o item não estiver na lista
        """
        if item not in self.items:
            raise ValueError("Item não encontrado na lista")
        
        idx = self.items.index(item)
        self.items[idx].remover_desconto()
        self._atualizar()

    def adicionar_nota_item(self, item: Item, nota: str) -> None:
        """
        Adiciona uma nota a um item específico.

        Args:
            item: O item a receber a nota
            nota: Texto da nota

        Raises:
            ValueError: Se o item não estiver na lista
        """
        if item not in self.items:
            raise ValueError("Item não encontrado na lista")
        
        idx = self.items.index(item)
        self.items[idx].adicionar_nota(nota)
        self._atualizar()

    def adicionar_nota_geral(self, nota: str) -> None:
        """
        Adiciona uma nota geral à lista.

        Args:
            nota: Texto da nota
        """
        if not nota:
            return
        if self.notas:
            self.notas = f"{self.notas}\n{nota}"
        else:
            self.notas = nota
        self._atualizar()

    @property
    def subtotal(self) -> Optional[Preco]:
        """
        Calcula o subtotal da lista (sem descontos).

        Returns:
            Optional[Preco]: O valor do subtotal ou None se a lista estiver vazia
        """
        if not self.items:
            return None
        return sum((item.subtotal for item in self.items), start=self.items[0].subtotal)

    @property
    def total_descontos(self) -> Optional[Preco]:
        """
        Calcula o total de descontos da lista.

        Returns:
            Optional[Preco]: O valor total dos descontos ou None se não houver
        """
        descontos = [item.valor_desconto for item in self.items if item.valor_desconto]
        if not descontos:
            return None
        return sum(descontos, start=descontos[0])

    @property
    def total(self) -> Optional[Preco]:
        """
        Calcula o valor total da lista.

        Returns:
            Optional[Preco]: O valor total considerando todos os itens e seus descontos
        """
        if not self.items:
            return None
        return sum((item.total for item in self.items), start=self.items[0].total)

    def agrupar_por_produto(self) -> Dict[str, List[Item]]:
        """
        Agrupa os itens da lista por produto.

        Returns:
            Dict[str, List[Item]]: Dicionário com SKU do produto como chave
            e lista de itens como valor
        """
        grupos: Dict[str, List[Item]] = {}
        for item in self.items:
            sku = item.produto.sku
            if sku not in grupos:
                grupos[sku] = []
            grupos[sku].append(item)
        return grupos

    def _atualizar(self) -> None:
        """Atualiza a data de última atualização da lista."""
        self.data_atualizacao = datetime.now()

    def __str__(self) -> str:
        """Retorna uma representação legível da lista de compras."""
        linhas = [f"Lista de Compras: {self.nome} ({self.id})"]
        if self.notas:
            linhas.append(f"Notas: {self.notas}")
        
        for item in self.items:
            linhas.append(f"- {item}")
        
        if self.total:
            if self.total_descontos:
                linhas.append(f"Subtotal: {self.subtotal}")
                linhas.append(f"Descontos: -{self.total_descontos}")
            linhas.append(f"Total: {self.total}")
        
        return "\n".join(linhas) 