"""
Router para endpoints de usuário.

Este módulo contém as rotas da API relacionadas a
operações com usuários.
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr

from src.joias.application.identity.user_service import (
    UserService,
    CriarUsuarioDTO,
    AtualizarUsuarioDTO,
    UsuarioDTO
)
from src.joias.infrastructure.persistence.sqlalchemy.repositories.usuario_repository import (
    SQLUsuarioRepository,
)
from src.joias.presentation.api.dependencies import get_db_session


class CriarUsuarioRequest(BaseModel):
    """Modelo de requisição para criar usuário."""
    nome: str
    email: EmailStr
    senha: str


class AtualizarUsuarioRequest(BaseModel):
    """Modelo de requisição para atualizar usuário."""
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    ativo: Optional[bool] = None


class UsuarioResponse(BaseModel):
    """Modelo de resposta com dados do usuário."""
    id: str
    nome: str
    email: str
    ativo: bool
    data_criacao: str


class ErrorResponse(BaseModel):
    """Modelo de resposta de erro."""
    erro: str


router = APIRouter(prefix="/api/usuarios", tags=["Usuários"])


@router.post(
    "",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {"model": ErrorResponse, "description": "Email já cadastrado"},
        400: {"model": ErrorResponse, "description": "Dados inválidos"}
    }
)
def criar_usuario(request: CriarUsuarioRequest, session=Depends(get_db_session)):
    """
    Cria um novo usuário.
    
    Args:
        request: Dados do usuário a ser criado
        session: Sessão do banco de dados
        
    Returns:
        Dados do usuário criado
        
    Raises:
        HTTPException: Se houver erro de validação ou conflito
    """
    try:
        service = UserService(SQLUsuarioRepository(session))
        dto = CriarUsuarioDTO(
            nome=request.nome,
            email=request.email,
            senha=request.senha
        )
        usuario = service.criar_usuario(dto)
        return usuario
    except ValueError as e:
        if "já cadastrado" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"erro": str(e)}
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"erro": str(e)}
        )


@router.get(
    "/{id}",
    response_model=UsuarioResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Usuário não encontrado"}
    }
)
def buscar_usuario(id: str, session=Depends(get_db_session)):
    """
    Busca um usuário pelo ID.
    
    Args:
        id: ID do usuário
        session: Sessão do banco de dados
        
    Returns:
        Dados do usuário
        
    Raises:
        HTTPException: Se o usuário não for encontrado
    """
    service = UserService(SQLUsuarioRepository(session))
    usuario = service.buscar_usuario(id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"erro": "Usuário não encontrado"}
        )
    return usuario


@router.get(
    "",
    response_model=List[UsuarioResponse]
)
def listar_usuarios(
    pagina: int = 1,
    tamanho: int = 10,
    email: Optional[str] = None,
    nome: Optional[str] = None,
    session=Depends(get_db_session)
):
    """
    Lista usuários com paginação e filtros.
    
    Args:
        pagina: Número da página
        tamanho: Quantidade de itens por página
        email: Filtro por email
        nome: Filtro por nome
        session: Sessão do banco de dados
        
    Returns:
        Lista de usuários
    """
    service = UserService(SQLUsuarioRepository(session))
    return service.listar_usuarios(
        pagina=pagina,
        tamanho=tamanho,
        email=email,
        nome=nome
    )


@router.put(
    "/{id}",
    response_model=UsuarioResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Usuário não encontrado"},
        409: {"model": ErrorResponse, "description": "Email já cadastrado"},
        400: {"model": ErrorResponse, "description": "Dados inválidos"}
    }
)
def atualizar_usuario(
    id: str,
    request: AtualizarUsuarioRequest,
    session=Depends(get_db_session)
):
    """
    Atualiza um usuário existente.
    
    Args:
        id: ID do usuário
        request: Dados do usuário a ser atualizado
        session: Sessão do banco de dados
        
    Returns:
        Dados do usuário atualizado
        
    Raises:
        HTTPException: Se houver erro de validação ou conflito
    """
    try:
        service = UserService(SQLUsuarioRepository(session))
        dto = AtualizarUsuarioDTO(
            id=id,
            nome=request.nome,
            email=request.email,
            ativo=request.ativo
        )
        usuario = service.atualizar_usuario(dto)
        return usuario
    except ValueError as e:
        if "não encontrado" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"erro": str(e)}
            )
        if "já cadastrado" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"erro": str(e)}
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"erro": str(e)}
        )


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"model": ErrorResponse, "description": "Usuário não encontrado"},
        409: {"model": ErrorResponse, "description": "Usuário possui dependências"}
    }
)
def excluir_usuario(id: str, session=Depends(get_db_session)):
    """
    Exclui um usuário existente.
    
    Args:
        id: ID do usuário
        session: Sessão do banco de dados
        
    Returns:
        Nada (204 No Content)
        
    Raises:
        HTTPException: Se o usuário não existir ou possuir dependências
    """
    try:
        service = UserService(SQLUsuarioRepository(session))
        service.excluir_usuario(id)
    except ValueError as e:
        if "não encontrado" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"erro": str(e)}
            )
        if "possui pedidos" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"erro": str(e)}
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"erro": str(e)}
        ) 