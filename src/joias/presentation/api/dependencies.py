"""
Dependências da API.

Este módulo contém as funções de injeção de dependência
utilizadas pelos endpoints da API.
"""
import os

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from ...application.identity.auth_service import AuthService
from ...application.identity.permissao_service import PermissaoService
from ...application.identity.usuario_service import UsuarioService
from ...application.shared.exceptions import AutenticacaoError
from ...domain.entities.usuario import Usuario
from ...domain.repositories.perfil_repository import IPerfilRepository
from ...domain.repositories.permissao_repository import IPermissaoRepository
from ...domain.repositories.usuario_repository import IUsuarioRepository
from ...infrastructure.config.settings import get_settings
from ...infrastructure.persistence.sqlalchemy.repositories.perfil_repository import (
    SQLPerfilRepository,
)
from ...infrastructure.persistence.sqlalchemy.repositories.permissao_repository import (
    SQLPermissaoRepository,
)
from ...infrastructure.persistence.sqlalchemy.repositories.usuario_repository import (
    SQLUsuarioRepository,
)
from ...infrastructure.persistence.sqlalchemy.session import get_db_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_permissao_repository(
    session: Session = Depends(get_db_session),
) -> IPermissaoRepository:
    """
    Retorna uma instância do repositório de permissões.

    Args:
        session: Sessão do banco de dados

    Returns:
        Repositório de permissões
    """
    return SQLPermissaoRepository(session)


def get_permissao_service(
    permissao_repository: IPermissaoRepository = Depends(get_permissao_repository),
) -> PermissaoService:
    """
    Retorna uma instância do serviço de permissões.

    Args:
        permissao_repository: Repositório de permissões

    Returns:
        Serviço de permissões
    """
    return PermissaoService(permissao_repository)


def get_perfil_repository(
    session: Session = Depends(get_db_session),
) -> IPerfilRepository:
    """
    Retorna uma instância do repositório de perfis.

    Args:
        session: Sessão do banco de dados

    Returns:
        Repositório de perfis
    """
    return SQLPerfilRepository(session)


def get_usuario_repository(
    session: Session = Depends(get_db_session),
) -> IUsuarioRepository:
    """
    Retorna uma instância do repositório de usuários.

    Args:
        session: Sessão do banco de dados

    Returns:
        Repositório de usuários
    """
    return SQLUsuarioRepository(session)


def get_auth_service(
    usuario_repository: IUsuarioRepository = Depends(get_usuario_repository),
) -> AuthService:
    """
    Retorna uma instância do serviço de autenticação.

    Args:
        usuario_repository: Repositório de usuários

    Returns:
        Serviço de autenticação
    """
    settings = get_settings()
    return AuthService(
        usuario_repository=usuario_repository,
        secret_key=settings.secret_key,
        token_expiration=settings.token_expiration,
    )


def get_usuario_service(
    usuario_repository: IUsuarioRepository = Depends(get_usuario_repository),
    auth_service: AuthService = Depends(get_auth_service),
) -> UsuarioService:
    """
    Retorna uma instância do serviço de usuários.

    Args:
        usuario_repository: Repositório de usuários
        auth_service: Serviço de autenticação

    Returns:
        Serviço de usuários
    """
    return UsuarioService(
        usuario_repository=usuario_repository,
        auth_service=auth_service,
    )


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
) -> Usuario:
    """
    Retorna o usuário autenticado.

    Args:
        token: Token JWT
        auth_service: Serviço de autenticação

    Returns:
        Usuário autenticado

    Raises:
        HTTPException: Se o token for inválido
    """
    try:
        return auth_service.validar_token(token)
    except AutenticacaoError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        ) 