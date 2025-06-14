"""
Router para endpoints de usuário.

Este módulo contém as rotas da API relacionadas a
operações com usuários.
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr

from ....application.identity.usuario_service import UsuarioService
from ....application.shared.exceptions import (
    EntidadeJaExisteError,
    EntidadeNaoEncontradaError,
    ValidacaoError,
)
from ....domain.entities.usuario import Usuario
from ..dependencies import get_current_user, get_usuario_service


class UsuarioBase(BaseModel):
    """
    Modelo base para usuário.
    """

    nome: str
    email: EmailStr


class UsuarioCreate(UsuarioBase):
    """
    Modelo para criação de usuário.
    """

    senha: str


class UsuarioUpdate(BaseModel):
    """
    Modelo para atualização de usuário.
    """

    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    ativo: Optional[bool] = None


class UsuarioResponse(UsuarioBase):
    """
    Modelo para resposta de usuário.
    """

    id: str
    ativo: bool
    data_criacao: str

    class Config:
        """
        Configuração do modelo.
        """

        from_attributes = True


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"],
)


def _usuario_to_response(usuario: Usuario) -> UsuarioResponse:
    """
    Converte um usuário para o modelo de resposta.

    Args:
        usuario: Usuário a ser convertido

    Returns:
        Modelo de resposta do usuário
    """
    return UsuarioResponse(
        id=str(usuario.id),
        nome=usuario.nome,
        email=str(usuario.email),
        ativo=usuario.ativo,
        data_criacao=usuario.data_criacao.isoformat(),
    )


@router.post(
    "",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
)
async def criar_usuario(
    usuario: UsuarioCreate,
    usuario_service: UsuarioService = Depends(get_usuario_service),
) -> UsuarioResponse:
    """
    Cria um novo usuário.

    Args:
        usuario: Dados do usuário
        usuario_service: Serviço de usuário

    Returns:
        Usuário criado

    Raises:
        HTTPException: Se houver erro na criação do usuário
    """
    try:
        usuario_criado = usuario_service.criar_usuario(
            nome=usuario.nome,
            email=usuario.email,
            senha=usuario.senha,
        )
        return _usuario_to_response(usuario_criado)
    except EntidadeJaExisteError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    except ValidacaoError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/{id}",
    response_model=UsuarioResponse,
)
async def buscar_usuario_por_id(
    id: str,
    usuario_service: UsuarioService = Depends(get_usuario_service),
    current_user: Usuario = Depends(get_current_user),
) -> UsuarioResponse:
    """
    Busca um usuário pelo ID.

    Args:
        id: ID do usuário
        usuario_service: Serviço de usuário
        current_user: Usuário autenticado

    Returns:
        Usuário encontrado

    Raises:
        HTTPException: Se o usuário não for encontrado
    """
    try:
        usuario = usuario_service.buscar_usuario_por_id(id)
        return _usuario_to_response(usuario)
    except EntidadeNaoEncontradaError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get(
    "",
    response_model=List[UsuarioResponse],
)
async def listar_usuarios(
    usuario_service: UsuarioService = Depends(get_usuario_service),
    current_user: Usuario = Depends(get_current_user),
) -> List[UsuarioResponse]:
    """
    Lista todos os usuários.

    Args:
        usuario_service: Serviço de usuário
        current_user: Usuário autenticado

    Returns:
        Lista de usuários
    """
    usuarios = usuario_service.listar_usuarios()
    return [_usuario_to_response(usuario) for usuario in usuarios]


@router.put(
    "/{id}",
    response_model=UsuarioResponse,
)
async def atualizar_usuario(
    id: str,
    usuario: UsuarioUpdate,
    usuario_service: UsuarioService = Depends(get_usuario_service),
    current_user: Usuario = Depends(get_current_user),
) -> UsuarioResponse:
    """
    Atualiza um usuário.

    Args:
        id: ID do usuário
        usuario: Dados do usuário
        usuario_service: Serviço de usuário
        current_user: Usuário autenticado

    Returns:
        Usuário atualizado

    Raises:
        HTTPException: Se houver erro na atualização do usuário
    """
    try:
        usuario_atualizado = usuario_service.atualizar_usuario(
            id=id,
            nome=usuario.nome,
            email=usuario.email,
            senha=usuario.senha,
            ativo=usuario.ativo,
        )
        return _usuario_to_response(usuario_atualizado)
    except EntidadeNaoEncontradaError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except EntidadeJaExisteError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    except ValidacaoError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def excluir_usuario(
    id: str,
    usuario_service: UsuarioService = Depends(get_usuario_service),
    current_user: Usuario = Depends(get_current_user),
) -> None:
    """
    Exclui um usuário.

    Args:
        id: ID do usuário
        usuario_service: Serviço de usuário
        current_user: Usuário autenticado

    Raises:
        HTTPException: Se o usuário não for encontrado
    """
    try:
        usuario_service.excluir_usuario(id)
    except EntidadeNaoEncontradaError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) 