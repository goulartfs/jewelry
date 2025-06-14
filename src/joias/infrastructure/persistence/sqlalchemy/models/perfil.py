"""
Modelo SQLAlchemy para Perfil.
"""
from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import relationship

from ..base import Base
from .perfil_permissao import perfil_permissao


class PerfilModel(Base):
    """Modelo SQLAlchemy para Perfil."""

    __tablename__ = "perfis"

    id = Column(String(36), primary_key=True)
    nome = Column(String(100), nullable=False, unique=True)
    descricao = Column(String(255))
    data_criacao = Column(DateTime, nullable=False)

    # Relacionamentos
    permissoes = relationship(
        "PermissaoModel",
        secondary=perfil_permissao,
        back_populates="perfis",
    ) 