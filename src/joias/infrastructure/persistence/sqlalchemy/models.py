"""
Modelos do SQLAlchemy.

Este módulo define os modelos do SQLAlchemy que mapeiam
as entidades do domínio para tabelas do banco de dados.
"""
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

# Cria a classe base para os modelos
Base = declarative_base()


class Usuario(Base):
    """Modelo para usuários do sistema."""

    __tablename__ = "usuarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    nome = Column(String(255), nullable=False)
    senha_hash = Column(String(255), nullable=False)
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relacionamentos
    perfis = relationship(
        "Perfil", secondary="usuario_perfil", back_populates="usuarios"
    )
    empresa_id = Column(UUID(as_uuid=True), ForeignKey("empresas.id"))
    empresa = relationship("Empresa", back_populates="usuarios")


class Empresa(Base):
    """Modelo para empresas."""

    __tablename__ = "empresas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(255), nullable=False)
    cnpj = Column(String(14), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relacionamentos
    usuarios = relationship("Usuario", back_populates="empresa")
    enderecos = relationship("Endereco", back_populates="empresa")


class Endereco(Base):
    """Modelo para endereços."""

    __tablename__ = "enderecos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    logradouro = Column(String(255), nullable=False)
    numero = Column(String(10), nullable=False)
    complemento = Column(String(255))
    bairro = Column(String(255), nullable=False)
    cidade = Column(String(255), nullable=False)
    estado = Column(String(2), nullable=False)
    cep = Column(String(8), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relacionamentos
    empresa_id = Column(UUID(as_uuid=True), ForeignKey("empresas.id"))
    empresa = relationship("Empresa", back_populates="enderecos")


class Perfil(Base):
    """Modelo para perfis de usuário."""

    __tablename__ = "perfis"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relacionamentos
    usuarios = relationship(
        "Usuario", secondary="usuario_perfil", back_populates="perfis"
    )
    permissoes = relationship(
        "Permissao", secondary="perfil_permissao", back_populates="perfis"
    )


class Permissao(Base):
    """Modelo para permissões."""

    __tablename__ = "permissoes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relacionamentos
    perfis = relationship(
        "Perfil", secondary="perfil_permissao", back_populates="permissoes"
    )


# Tabelas de associação para relacionamentos many-to-many
usuario_perfil = Table(
    "usuario_perfil",
    Base.metadata,
    Column("usuario_id", UUID(as_uuid=True), ForeignKey("usuarios.id")),
    Column("perfil_id", UUID(as_uuid=True), ForeignKey("perfis.id")),
)

perfil_permissao = Table(
    "perfil_permissao",
    Base.metadata,
    Column("perfil_id", UUID(as_uuid=True), ForeignKey("perfis.id")),
    Column("permissao_id", UUID(as_uuid=True), ForeignKey("permissoes.id")),
)
