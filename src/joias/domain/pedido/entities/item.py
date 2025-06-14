"""
Entidade que representa um item de pedido.

Este módulo define a estrutura e comportamento de um item que pode
ser parte de um pedido ou lista de compras.
"""
from dataclasses import dataclass
from typing import Optional
from decimal import Decimal

from ...catalogo.entities.produto import Produto
from ...shared.value_objects.preco import Preco


@dataclass
class Item:
    """
    Representa um item que pode ser parte de um pedido ou lista de compras.

    Esta é uma entidade que encapsula um produto, sua quantidade, preço
    e outras informações relevantes para o contexto de compra.

    Attributes:
        produto: O produto associado ao item
        quantidade: A quantidade do item
        preco_unitario: O preço unitário do item
        desconto_percentual: Desconto percentual aplicado ao item (0-100)
        notas: Observações ou especificações especiais para o item
    """
    produto: Produto
    quantidade: int
    preco_unitario: Preco
    desconto_percentual: Optional[Decimal] = None
    notas: Optional[str] = None

    def __post_init__(self):
        """Validação após inicialização do item."""
        if self.quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero")
        
        if self.desconto_percentual is not None:
            if not isinstance(self.desconto_percentual, Decimal):
                self.desconto_percentual = Decimal(str(self.desconto_percentual))
            if not 0 <= self.desconto_percentual <= 100:
                raise ValueError("O desconto deve estar entre 0 e 100")

    @property
    def subtotal(self) -> Preco:
        """
        Calcula o subtotal do item (preço unitário * quantidade).

        Returns:
            Preco: O valor do subtotal
        """
        return self.preco_unitario * self.quantidade

    @property
    def valor_desconto(self) -> Optional[Preco]:
        """
        Calcula o valor do desconto, se houver.

        Returns:
            Optional[Preco]: O valor do desconto ou None se não houver
        """
        if self.desconto_percentual is None or self.desconto_percentual == 0:
            return None
        return self.subtotal * (self.desconto_percentual / 100)

    @property
    def total(self) -> Preco:
        """
        Calcula o total do item considerando o desconto, se houver.

        Returns:
            Preco: O valor total do item
        """
        if self.desconto_percentual is None or self.desconto_percentual == 0:
            return self.subtotal
        
        desconto = self.valor_desconto
        return self.subtotal - desconto if desconto else self.subtotal

    def aplicar_desconto(self, percentual: Decimal) -> None:
        """
        Aplica um desconto percentual ao item.

        Args:
            percentual: Valor do desconto (0-100)

        Raises:
            ValueError: Se o percentual não estiver entre 0 e 100
        """
        if not isinstance(percentual, Decimal):
            percentual = Decimal(str(percentual))
        if not 0 <= percentual <= 100:
            raise ValueError("O desconto deve estar entre 0 e 100")
        self.desconto_percentual = percentual

    def remover_desconto(self) -> None:
        """Remove o desconto aplicado ao item."""
        self.desconto_percentual = None

    def atualizar_quantidade(self, nova_quantidade: int) -> None:
        """
        Atualiza a quantidade do item.

        Args:
            nova_quantidade: Nova quantidade

        Raises:
            ValueError: Se a quantidade for menor ou igual a zero
        """
        if nova_quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero")
        self.quantidade = nova_quantidade

    def adicionar_nota(self, nota: str) -> None:
        """
        Adiciona uma nota ao item.

        Args:
            nota: Texto da nota
        """
        if not nota:
            return
        if self.notas:
            self.notas = f"{self.notas}\n{nota}"
        else:
            self.notas = nota

    def __str__(self) -> str:
        """Retorna uma representação legível do item."""
        base = f"{self.quantidade}x {self.produto.nome} @ {self.preco_unitario}"
        if self.desconto_percentual:
            base += f" (-{self.desconto_percentual}%)"
        base += f" = {self.total}"
        if self.notas:
            base += f" [{self.notas}]"
        return base 