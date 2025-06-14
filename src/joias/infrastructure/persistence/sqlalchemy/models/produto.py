"""
Modelo SQLAlchemy para produtos.

Este módulo define o modelo de dados para produtos usando SQLAlchemy ORM.
"""
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from ..base import Base


class ProdutoModel(Base):
    """Modelo SQLAlchemy para a tabela de produtos."""
    __tablename__ = 'produtos'

    id = Column(Integer, primary_key=True)
    sku = Column(String(50), unique=True, nullable=False)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(500))
    preco_valor = Column(Numeric(10, 2), nullable=False)
    preco_moeda = Column(String(3), nullable=False)
    preco_data_inicio = Column(DateTime, nullable=False, default=datetime.now)
    preco_data_fim = Column(DateTime)
    data_criacao = Column(DateTime, nullable=False, default=datetime.now)
    ativo = Column(Boolean, nullable=False, default=True)

    # Relacionamentos
    variacoes = relationship('VariacaoModel', back_populates='produto')
    detalhes = relationship('DetalheModel', back_populates='produto')


class VariacaoModel(Base):
    """Modelo SQLAlchemy para a tabela de variações de produtos."""
    __tablename__ = 'variacoes'

    id = Column(Integer, primary_key=True)
    produto_id = Column(Integer, ForeignKey('produtos.id'), nullable=False)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(500))
    codigo = Column(String(50), nullable=False)
    data_criacao = Column(DateTime, nullable=False, default=datetime.now)
    ativo = Column(Boolean, nullable=False, default=True)

    # Relacionamentos
    produto = relationship('ProdutoModel', back_populates='variacoes')
    detalhes = relationship('DetalheVariacaoModel', back_populates='variacao')


class DetalheModel(Base):
    """Modelo SQLAlchemy para a tabela de detalhes de produtos."""
    __tablename__ = 'detalhes'

    id = Column(Integer, primary_key=True)
    produto_id = Column(Integer, ForeignKey('produtos.id'), nullable=False)
    nome = Column(String(100), nullable=False)
    valor = Column(String(200), nullable=False)
    tipo = Column(String(50), nullable=False)
    data_criacao = Column(DateTime, nullable=False, default=datetime.now)
    ativo = Column(Boolean, nullable=False, default=True)

    # Relacionamentos
    produto = relationship('ProdutoModel', back_populates='detalhes')


class DetalheVariacaoModel(Base):
    """Modelo SQLAlchemy para a tabela de detalhes de variações."""
    __tablename__ = 'detalhes_variacoes'

    id = Column(Integer, primary_key=True)
    variacao_id = Column(Integer, ForeignKey('variacoes.id'), nullable=False)
    nome = Column(String(100), nullable=False)
    valor = Column(String(200), nullable=False)
    tipo = Column(String(50), nullable=False)
    data_criacao = Column(DateTime, nullable=False, default=datetime.now)
    ativo = Column(Boolean, nullable=False, default=True)

    # Relacionamentos
    variacao = relationship('VariacaoModel', back_populates='detalhes') 