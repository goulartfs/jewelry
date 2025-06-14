"""
DTOs para operações com Permissão.
"""
from typing import Optional

from pydantic import BaseModel, Field


class CriarPermissaoDTO(BaseModel):
    """DTO para criação de uma nova permissão."""

    nome: str = Field(..., description="Nome descritivo da permissão")
    chave: str = Field(..., description="Chave única usada no código")
    descricao: Optional[str] = Field(None, description="Descrição detalhada")


class AtualizarPermissaoDTO(BaseModel):
    """DTO para atualização de uma permissão."""

    nome: Optional[str] = None
    chave: Optional[str] = None
    descricao: Optional[str] = None


class PermissaoDTO(BaseModel):
    """DTO para retorno de dados de uma permissão."""

    id: str = Field(..., description="ID da permissão")
    nome: str = Field(..., description="Nome descritivo da permissão")
    chave: str = Field(..., description="Chave única usada no código")
    descricao: Optional[str] = Field(None, description="Descrição detalhada") 