"""
DTOs para operações com Perfil.
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from .permissao import PermissaoDTO


class CriarPerfilDTO(BaseModel):
    """DTO para criação de um novo perfil."""

    nome: str = Field(..., description="Nome do perfil")
    descricao: Optional[str] = Field(None, description="Descrição detalhada")


class AtualizarPerfilDTO(BaseModel):
    """DTO para atualização de um perfil."""

    nome: Optional[str] = None
    descricao: Optional[str] = None


class PerfilDTO(BaseModel):
    """DTO para retorno de dados de um perfil."""

    id: str = Field(..., description="ID do perfil")
    nome: str = Field(..., description="Nome do perfil")
    descricao: Optional[str] = Field(None, description="Descrição detalhada")
    permissoes: List[PermissaoDTO] = Field(default_factory=list, description="Lista de permissões")
    data_criacao: datetime = Field(..., description="Data de criação do perfil") 