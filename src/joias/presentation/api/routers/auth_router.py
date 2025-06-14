"""
Router para endpoints de autenticação.
"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from ....application.identity.auth_service import AuthService
from ....application.shared.exceptions import AutenticacaoError, ValidacaoError
from ....domain.entities.usuario import Usuario
from ..dependencies import get_auth_service, get_current_user


class Token(BaseModel):
    """
    Modelo para token de acesso.
    """

    access_token: str
    token_type: str


class UsuarioLogado(BaseModel):
    """
    Modelo para usuário logado.
    """

    id: str
    nome: str
    email: str
    ativo: bool

    class Config:
        """
        Configuração do modelo.
        """

        from_attributes = True


router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"],
)


@router.post(
    "/login",
    response_model=Token,
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
) -> Token:
    """
    Autentica um usuário.

    Args:
        form_data: Dados do formulário de login
        auth_service: Serviço de autenticação

    Returns:
        Token de acesso

    Raises:
        HTTPException: Se as credenciais forem inválidas
    """
    try:
        token = auth_service.autenticar(
            email=form_data.username,
            senha=form_data.password,
        )
        return Token(
            access_token=token,
            token_type="bearer",
        )
    except (AutenticacaoError, ValidacaoError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get(
    "/me",
    response_model=UsuarioLogado,
)
async def me(
    usuario: Usuario = Depends(get_current_user),
) -> UsuarioLogado:
    """
    Retorna o usuário logado.

    Args:
        usuario: Usuário logado

    Returns:
        Dados do usuário logado
    """
    return UsuarioLogado(
        id=str(usuario.id),
        nome=usuario.nome,
        email=str(usuario.email),
        ativo=usuario.ativo,
    ) 