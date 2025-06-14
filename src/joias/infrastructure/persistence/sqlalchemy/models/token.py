"""
Modelo SQLAlchemy para tokens.

Este módulo define o modelo de tokens usando
SQLAlchemy como ORM.
"""
from datetime import datetime
from uuid import UUID

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import relationship

from src.joias.infrastructure.persistence.sqlalchemy.base import Base


class Token(Base):
    """Modelo SQLAlchemy para tokens."""

    __tablename__ = "token"

    id = Column(PgUUID(as_uuid=True), primary_key=True)
    usuario_id = Column(PgUUID(as_uuid=True), ForeignKey("usuario.id"), nullable=False)
    token = Column(String(255), nullable=False, unique=True)
    expiracao = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relacionamento com usuário
    usuario = relationship("Usuario", back_populates="tokens") 