"""
Schemas para usuários.

Este módulo define os schemas Pydantic para validação
e serialização de dados de usuários na API.
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, constr


class UserBase(BaseModel):
    """
    Schema base para usuários.

    Attributes:
        email: Email do usuário
        nome: Nome completo do usuário
    """

    email: EmailStr
    nome: constr(min_length=3, max_length=255)


class UserCreate(UserBase):
    """
    Schema para criação de usuário.

    Attributes:
        senha: Senha do usuário
    """

    senha: constr(min_length=8, max_length=255)


class UserUpdate(BaseModel):
    """
    Schema para atualização de usuário.

    Attributes:
        email: Novo email do usuário
        nome: Novo nome do usuário
        senha: Nova senha do usuário
    """

    email: Optional[EmailStr] = None
    nome: Optional[constr(min_length=3, max_length=255)] = None
    senha: Optional[constr(min_length=8, max_length=255)] = None


class UserResponse(UserBase):
    """
    Schema para resposta de usuário.

    Attributes:
        id: ID do usuário
        ativo: Se o usuário está ativo
        empresa_id: ID da empresa do usuário
        created_at: Data de criação
        updated_at: Data da última atualização
        deleted_at: Data de exclusão
    """

    id: str
    ativo: bool
    empresa_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        """Configuração do Pydantic."""

        orm_mode = True


class UserList(BaseModel):
    """
    Schema para lista de usuários.

    Attributes:
        items: Lista de usuários
        total: Total de usuários
        skip: Número de registros pulados
        limit: Número máximo de registros
    """

    items: List[UserResponse]
    total: int
    skip: int
    limit: int
