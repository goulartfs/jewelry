"""
Modelos de dados para o módulo alpha.

Este módulo contém as definições das entidades principais do sistema,
incluindo usuários, contatos, dados pessoais, endereços, etc.
"""
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List, Optional


@dataclass
class Endereco:
    """Representa um endereço físico no sistema."""

    id: int
    logradouro: str
    numero: str
    complemento: Optional[str]
    bairro: str
    cidade: str
    estado: str
    cep: str
    pais: str = "Brasil"
    data_criacao: datetime = field(default_factory=datetime.now)
    ativo: bool = True


@dataclass
class DadoPessoal:
    """Representa os dados pessoais de um indivíduo."""

    id: int
    nome: str
    cpf: str
    rg: Optional[str]
    data_nascimento: datetime
    enderecos: List[Endereco] = field(default_factory=list)
    data_criacao: datetime = field(default_factory=datetime.now)
    ativo: bool = True


@dataclass
class Contato:
    """Representa informações de contato."""

    id: int
    email: str
    telefone: str
    dados_pessoais: List[DadoPessoal] = field(default_factory=list)
    data_criacao: datetime = field(default_factory=datetime.now)
    ativo: bool = True


@dataclass
class Empresa:
    """Representa uma organização ou negócio."""

    id: int
    razao_social: str
    nome_fantasia: str
    cnpj: str
    inscricao_estadual: Optional[str]
    inscricao_municipal: Optional[str]
    endereco: Endereco
    contato: Contato
    data_criacao: datetime = field(default_factory=datetime.now)
    ativo: bool = True


@dataclass
class Permissao:
    """Representa uma permissão no sistema."""

    id: int
    nome: str
    descricao: str
    codigo: str
    data_criacao: datetime = field(default_factory=datetime.now)
    ativo: bool = True


@dataclass
class Perfil:
    """Define um conjunto de permissões para usuários."""

    id: int
    nome: str
    descricao: str
    permissoes: List[Permissao] = field(default_factory=list)
    data_criacao: datetime = field(default_factory=datetime.now)
    ativo: bool = True


@dataclass
class Usuario:
    """Representa um usuário do sistema."""

    id: int
    username: str
    email: str
    senha_hash: str
    perfil: Perfil
    dados_pessoais: DadoPessoal
    empresa: Optional[Empresa]
    data_ultimo_acesso: Optional[datetime]
    data_criacao: datetime = field(default_factory=datetime.now)
    ativo: bool = True


@dataclass
class Preco:
    """Representa o preço de um produto."""

    id: int
    valor: Decimal
    moeda: str = "BRL"
    data_inicio: datetime = field(default_factory=datetime.now)
    data_fim: Optional[datetime] = None
    data_criacao: datetime = field(default_factory=datetime.now)
    ativo: bool = True


@dataclass
class Detalhe:
    """Contém informações detalhadas sobre um produto."""

    id: int
    nome: str
    valor: str
    tipo: str
    data_criacao: datetime = field(default_factory=datetime.now)
    ativo: bool = True


@dataclass
class Variacao:
    """Representa uma variação específica de um produto."""

    id: int
    nome: str
    descricao: str
    codigo: str
    detalhes: List[Detalhe] = field(default_factory=list)
    data_criacao: datetime = field(default_factory=datetime.now)
    ativo: bool = True


@dataclass
class Produto:
    """Representa um produto que pode ser vendido."""

    id: int
    nome: str
    descricao: str
    codigo: str
    preco: Preco
    variacoes: List[Variacao] = field(default_factory=list)
    detalhes: List[Detalhe] = field(default_factory=list)
    data_criacao: datetime = field(default_factory=datetime.now)
    ativo: bool = True


@dataclass
class Catalogo:
    """Representa uma coleção de produtos."""

    id: int
    nome: str
    descricao: str
    usuario: Usuario
    produtos: List[Produto] = field(default_factory=list)
    data_inicio: datetime = field(default_factory=datetime.now)
    data_fim: Optional[datetime] = None
    data_criacao: datetime = field(default_factory=datetime.now)
    ativo: bool = True


@dataclass
class ItemPedido:
    """Representa um item específico em um pedido."""

    id: int
    produto: Produto
    quantidade: int
    preco_unitario: Decimal
    desconto: Decimal = Decimal("0")
    data_criacao: datetime = field(default_factory=datetime.now)
    ativo: bool = True

    @property
    def subtotal(self) -> Decimal:
        """Calcula o subtotal do item (preço * quantidade - desconto)."""
        return (self.preco_unitario * self.quantidade) - self.desconto


@dataclass
class Pedido:
    """Representa um pedido no sistema."""

    id: int
    usuario: Usuario
    itens: List[ItemPedido] = field(default_factory=list)
    status: str = "rascunho"  # rascunho, confirmado, pago, cancelado, entregue
    data_confirmacao: Optional[datetime] = None
    data_pagamento: Optional[datetime] = None
    data_cancelamento: Optional[datetime] = None
    data_entrega: Optional[datetime] = None
    data_criacao: datetime = field(default_factory=datetime.now)
    ativo: bool = True

    @property
    def total(self) -> Decimal:
        """Calcula o valor total do pedido."""
        return sum(item.subtotal for item in self.itens)
