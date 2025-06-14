"""
Modelo SQLAlchemy para fornecedores.

Este módulo contém os modelos SQLAlchemy que representam as tabelas
de fornecedores e documentos no banco de dados.
"""
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from .base import Base


class Fornecedor(Base):
    """Modelo SQLAlchemy para a tabela de fornecedores."""

    __tablename__ = "fornecedores"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    logradouro = Column(String(100), nullable=False)
    numero = Column(String(10), nullable=False)
    bairro = Column(String(50), nullable=False)
    cidade = Column(String(50), nullable=False)
    estado = Column(String(2), nullable=False)
    cep = Column(String(9), nullable=False)
    complemento = Column(String(100))
    pais = Column(String(50), default="Brasil")
    ativo = Column(Boolean, default=True)
    data_cadastro = Column(DateTime, default=datetime.now)

    # Relacionamentos
    documentos = relationship(
        "Documento", back_populates="fornecedor", cascade="all, delete-orphan"
    )
    produtos = relationship(
        "Produto", secondary="fornecedores_produtos", back_populates="fornecedores"
    )


class Documento(Base):
    """Modelo SQLAlchemy para a tabela de documentos."""

    __tablename__ = "documentos"

    id = Column(Integer, primary_key=True)
    numero = Column(String(20), nullable=False)
    tipo = Column(String(10), nullable=False)
    fornecedor_id = Column(Integer, ForeignKey("fornecedores.id"), nullable=False)

    # Relacionamentos
    fornecedor = relationship("Fornecedor", back_populates="documentos")


# Tabela de associação entre fornecedores e produtos
fornecedores_produtos = Table(
    "fornecedores_produtos",
    Base.metadata,
    Column("fornecedor_id", Integer, ForeignKey("fornecedores.id"), primary_key=True),
    Column("produto_id", Integer, ForeignKey("produtos.id"), primary_key=True),
)
