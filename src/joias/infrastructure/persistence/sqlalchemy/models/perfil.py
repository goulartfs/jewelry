"""
Modelo SQLAlchemy para perfis.

Este módulo define o modelo de perfis usando
SQLAlchemy como ORM.
"""
from datetime import datetime
from uuid import UUID

from sqlalchemy import Column, DateTime, String, Table, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import relationship

from src.joias.infrastructure.persistence.sqlalchemy.base import Base


# Tabela de associação entre usuários e perfis
usuario_perfil = Table(
    "usuario_perfil",
    Base.metadata,
    Column("usuario_id", PgUUID(as_uuid=True), ForeignKey("usuario.id"), primary_key=True),
    Column("perfil_id", PgUUID(as_uuid=True), ForeignKey("perfil.id"), primary_key=True),
)


class Perfil(Base):
    """Modelo SQLAlchemy para perfis."""

    __tablename__ = "perfil"

    id = Column(PgUUID(as_uuid=True), primary_key=True)
    nome = Column(String(100), nullable=False, unique=True)
    descricao = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relacionamento many-to-many com usuários
    usuarios = relationship(
        "Usuario",
        secondary=usuario_perfil,
        back_populates="perfis",
    ) 