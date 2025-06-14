"""
Router para endpoints de perfil.

Este módulo contém as rotas da API relacionadas a
operações com perfis de usuário.
"""
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from src.joias.application.identity.perfil_service import (
    PerfilService,
    CriarPerfilDTO,
    AtualizarPerfilDTO,
    PerfilDTO
)
from src.joias.infrastructure.persistence.sqlalchemy.repositories.perfil_repository import (
    SQLPerfilRepository,
)
from src.joias.presentation.api.dependencies import get_db_session


router = APIRouter(prefix="/api/perfis", tags=["Perfis"])


class ErrorResponse(BaseModel):
    """Modelo de resposta de erro."""
    erro: str


class CriarPerfilRequest(BaseModel):
    """Modelo de requisição para criar perfil."""
    nome: str
    descricao: Optional[str] = None


class PerfilResponse(BaseModel):
    """Modelo de resposta com dados do perfil."""
    id: UUID
    nome: str
    descricao: Optional[str] = None
    created_at: str
    updated_at: str


@router.post(
    "",
    response_model=PerfilResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {"model": ErrorResponse, "description": "Nome de perfil já existe"},
        400: {"model": ErrorResponse, "description": "Dados inválidos"}
    }
)
def criar_perfil(request: CriarPerfilRequest, session=Depends(get_db_session)):
    """
    Cria um novo perfil.
    
    Args:
        request: Dados do perfil a ser criado
        session: Sessão do banco de dados
        
    Returns:
        Dados do perfil criado
        
    Raises:
        HTTPException: Se houver erro de validação ou conflito
    """
    try:
        service = PerfilService(SQLPerfilRepository(session))
        dto = CriarPerfilDTO(
            nome=request.nome,
            descricao=request.descricao
        )
        perfil = service.criar_perfil(dto)
        return perfil
    except ValueError as e:
        if "já existe" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"erro": str(e)}
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"erro": str(e)}
        )


@router.put(
    "/{id}/usuarios/{usuario_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"model": ErrorResponse, "description": "Perfil ou usuário não encontrado"},
        400: {"model": ErrorResponse, "description": "Dados inválidos"}
    }
)
def associar_usuario(
    id: UUID,
    usuario_id: UUID,
    session=Depends(get_db_session)
):
    """
    Associa um usuário a um perfil.
    
    Args:
        id: ID do perfil
        usuario_id: ID do usuário
        session: Sessão do banco de dados
        
    Raises:
        HTTPException: Se houver erro de validação ou recurso não encontrado
    """
    try:
        service = PerfilService(SQLPerfilRepository(session))
        service.associar_usuario(id, usuario_id)
    except ValueError as e:
        if "não encontrado" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"erro": str(e)}
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"erro": str(e)}
        ) 