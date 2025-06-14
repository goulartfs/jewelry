"""
Entidade que representa um produto no catálogo.

Esta é uma entidade do domínio que representa um produto que pode ser
vendido, com suas características e preço.
"""
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

from ...shared.value_objects.preco import Preco


@dataclass
class Detalhe:
    """Representa um detalhe específico do produto."""
    nome: str
    valor: str
    tipo: str
    data_criacao: datetime = field(default_factory=datetime.now)
    ativo: bool = True


@dataclass
class Variacao:
    """Representa uma variação específica do produto."""
    nome: str
    descricao: str
    codigo: str
    detalhes: List[Detalhe] = field(default_factory=list)
    data_criacao: datetime = field(default_factory=datetime.now)
    ativo: bool = True


@dataclass
class Produto:
    """
    Representa um produto no catálogo.

    Esta é uma entidade rica que encapsula toda a lógica relacionada
    a um produto, incluindo suas variações, detalhes e preço.

    Atributos:
        sku (str): Código identificador único do produto
        nome (str): Nome do produto
        descricao (str): Descrição detalhada do produto
        preco (Preco): Preço atual do produto
        variacoes (List[Variacao]): Lista de variações do produto
        detalhes (List[Detalhe]): Lista de detalhes do produto
        data_criacao (datetime): Data de criação do produto
        ativo (bool): Indica se o produto está ativo
    """
    sku: str
    nome: str
    descricao: str
    preco: Preco
    variacoes: List[Variacao] = field(default_factory=list)
    detalhes: List[Detalhe] = field(default_factory=list)
    data_criacao: datetime = field(default_factory=datetime.now)
    ativo: bool = True

    def adicionar_variacao(self, variacao: Variacao) -> None:
        """
        Adiciona uma nova variação ao produto.

        Args:
            variacao: A variação a ser adicionada
        """
        self.variacoes.append(variacao)

    def adicionar_detalhe(self, detalhe: Detalhe) -> None:
        """
        Adiciona um novo detalhe ao produto.

        Args:
            detalhe: O detalhe a ser adicionado
        """
        self.detalhes.append(detalhe)

    def atualizar_preco(self, novo_preco: Preco) -> None:
        """
        Atualiza o preço do produto.

        Args:
            novo_preco: O novo preço do produto
        """
        self.preco = novo_preco

    def desativar(self) -> None:
        """Desativa o produto."""
        self.ativo = False

    def ativar(self) -> None:
        """Ativa o produto."""
        self.ativo = True

    def __repr__(self) -> str:
        """Retorna uma representação string do produto."""
        status = "ativo" if self.ativo else "inativo"
        return f"{self.nome} ({self.sku}): {self.preco} - {status}" 