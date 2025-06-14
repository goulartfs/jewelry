"""
Entidades relacionadas a produtos.

Este módulo contém as entidades que representam produtos,
suas variações, detalhes e preços.
"""
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from .base import Entity


@dataclass
class Preco(Entity):
    """
    Entidade que representa o preço de um produto.
    
    Um preço tem um valor monetário e um período de validade.
    """
    valor: Decimal
    moeda: str = "BRL"
    data_inicio: datetime = field(default_factory=datetime.now)
    data_fim: Optional[datetime] = None

    def esta_vigente(self, data: Optional[datetime] = None) -> bool:
        """
        Verifica se o preço está vigente em uma determinada data.

        Args:
            data: Data a ser verificada (usa a data atual se None)

        Returns:
            True se o preço está vigente, False caso contrário
        """
        data = data or datetime.now()
        if not self.ativo:
            return False
        if data < self.data_inicio:
            return False
        if self.data_fim and data > self.data_fim:
            return False
        return True

    def formatar(self) -> str:
        """
        Retorna o preço formatado como string.

        Returns:
            String formatada com o valor e a moeda
        """
        return f"{self.moeda} {self.valor:.2f}"


@dataclass
class Detalhe(Entity):
    """
    Entidade que representa um detalhe de produto.
    
    Um detalhe é uma característica específica de um produto,
    como material, cor, etc.
    """
    nome: str
    valor: str
    tipo: str

    def __eq__(self, other):
        if not isinstance(other, Detalhe):
            return NotImplemented
        return (
            self.nome == other.nome and
            self.valor == other.valor and
            self.tipo == other.tipo
        )

    def __hash__(self):
        return hash((self.nome, self.valor, self.tipo))


@dataclass
class Variacao(Entity):
    """
    Entidade que representa uma variação de produto.
    
    Uma variação é uma versão específica de um produto,
    como tamanho, modelo, etc.
    """
    nome: str
    descricao: str
    codigo: str
    detalhes: List[Detalhe] = field(default_factory=list)

    def adicionar_detalhe(self, detalhe: Detalhe) -> None:
        """
        Adiciona um detalhe à variação.

        Args:
            detalhe: Detalhe a ser adicionado
        """
        if detalhe not in self.detalhes:
            self.detalhes.append(detalhe)
            self.atualizar()

    def remover_detalhe(self, detalhe: Detalhe) -> None:
        """
        Remove um detalhe da variação.

        Args:
            detalhe: Detalhe a ser removido
        """
        if detalhe in self.detalhes:
            self.detalhes.remove(detalhe)
            self.atualizar()


@dataclass
class Produto(Entity):
    """
    Entidade que representa um produto.
    
    Um produto é um item que pode ser vendido e pode ter
    diferentes variações e detalhes.
    """
    nome: str
    descricao: str
    codigo: str
    preco: Preco
    variacoes: List[Variacao] = field(default_factory=list)
    detalhes: List[Detalhe] = field(default_factory=list)

    def adicionar_variacao(self, variacao: Variacao) -> None:
        """
        Adiciona uma variação ao produto.

        Args:
            variacao: Variação a ser adicionada
        """
        if variacao not in self.variacoes:
            self.variacoes.append(variacao)
            self.atualizar()

    def remover_variacao(self, variacao_id: int) -> None:
        """
        Remove uma variação do produto.

        Args:
            variacao_id: ID da variação a ser removida
        """
        self.variacoes = [
            v for v in self.variacoes
            if v.id != variacao_id
        ]
        self.atualizar()

    def adicionar_detalhe(self, detalhe: Detalhe) -> None:
        """
        Adiciona um detalhe ao produto.

        Args:
            detalhe: Detalhe a ser adicionado
        """
        if detalhe not in self.detalhes:
            self.detalhes.append(detalhe)
            self.atualizar()

    def remover_detalhe(self, detalhe: Detalhe) -> None:
        """
        Remove um detalhe do produto.

        Args:
            detalhe: Detalhe a ser removido
        """
        if detalhe in self.detalhes:
            self.detalhes.remove(detalhe)
            self.atualizar()

    def atualizar_preco(self, preco: Preco) -> None:
        """
        Atualiza o preço do produto.

        Args:
            preco: Novo preço
        """
        self.preco = preco
        self.atualizar() 