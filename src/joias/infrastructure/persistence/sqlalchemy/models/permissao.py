"""
Modelo SQLAlchemy para Permissão.
"""
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from ..base import Base
from .perfil_permissao import perfil_permissao


class PermissaoModel(Base):
    """Modelo SQLAlchemy para Permissão."""

    __tablename__ = "permissoes"

    id = Column(String(36), primary_key=True)
    nome = Column(String(100), nullable=False)
    chave = Column(String(50), nullable=False, unique=True)
    descricao = Column(String(255))

    # Relacionamentos
    perfis = relationship(
        "PerfilModel",
        secondary=perfil_permissao,
        back_populates="permissoes",
    ) 