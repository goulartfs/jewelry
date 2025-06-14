"""
DTOs para produtos.

Este módulo contém os DTOs (Data Transfer Objects) usados para transferir
dados de produtos entre as camadas da aplicação.
"""
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List, Optional


@dataclass
class PrecoDTO:
    """DTO para preços."""

    valor: Decimal
    moeda: str
    data_inicio: datetime
    data_fim: Optional[datetime] = None


@dataclass
class DetalheDTO:
    """DTO para detalhes."""

    nome: str
    valor: str
    tipo: str


@dataclass
class VariacaoDTO:
    """DTO para variações."""

    nome: str
    descricao: str
    codigo: str
    detalhes: List[DetalheDTO]


@dataclass
class ProdutoDTO:
    """DTO para produtos."""

    sku: str
    nome: str
    descricao: str
    preco: PrecoDTO
    variacoes: List[VariacaoDTO]
    detalhes: List[DetalheDTO]


@dataclass
class CriarProdutoDTO:
    """DTO para criação de produtos."""

    sku: str
    nome: str
    descricao: str
    preco_valor: Decimal
    preco_moeda: str = "BRL"


@dataclass
class AtualizarProdutoDTO:
    """DTO para atualização de produtos."""

    nome: Optional[str] = None
    descricao: Optional[str] = None
    preco_valor: Optional[Decimal] = None
    preco_moeda: Optional[str] = None


@dataclass
class ListagemProdutoDTO:
    """DTO para listagem de produtos."""

    sku: str
    nome: str
    preco_valor: Decimal
    preco_moeda: str
    ativo: bool
