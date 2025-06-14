"""
Tabela de associação entre Perfil e Permissão.
"""
from sqlalchemy import Column, ForeignKey, String, Table

from ..base import Base

perfil_permissao = Table(
    "perfil_permissao",
    Base.metadata,
    Column("perfil_id", String(36), ForeignKey("perfis.id"), primary_key=True),
    Column("permissao_id", String(36), ForeignKey("permissoes.id"), primary_key=True),
) 