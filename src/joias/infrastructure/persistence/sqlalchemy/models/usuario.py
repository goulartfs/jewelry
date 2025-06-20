"""
Modelo SQLAlchemy para usuários.

Este módulo define o modelo de usuários usando
SQLAlchemy como ORM.
"""
from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import relationship

from src.joias.infrastructure.persistence.sqlalchemy.base import Base
from src.joias.infrastructure.persistence.sqlalchemy.models.perfil import usuario_perfil


class UsuarioModel(Base):
    """
    Modelo SQLAlchemy para usuários.
    """

    __tablename__ = "usuarios"

    id = Column(PgUUID(as_uuid=True), primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    senha_hash = Column(String(255), nullable=False)
    ativo = Column(Boolean, nullable=False, default=True)
    data_criacao = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relacionamento many-to-many com perfis
    perfis = relationship(
        "Perfil",
        secondary=usuario_perfil,
        back_populates="usuarios",
    )

    # Relacionamento one-to-many com tokens
    tokens = relationship("Token", back_populates="usuario", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        """Retorna uma representação legível do modelo."""
        return f"<Usuario {self.nome} ({self.email})>"
