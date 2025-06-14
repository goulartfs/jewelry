"""
Dependências de autenticação.

Este módulo define as dependências do FastAPI relacionadas
à autenticação e autorização.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from ....infrastructure.persistence.sqlalchemy.session import get_db
from ....application.identity.auth_service import AuthService
from ....domain.identity.entities.usuario import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Usuario:
    """
    Retorna o usuário atual baseado no token JWT.

    Args:
        token: Token de acesso
        db: Sessão do banco de dados

    Returns:
        Usuario: Usuário autenticado

    Raises:
        HTTPException: Se o token for inválido ou o usuário não for encontrado
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    auth_service = AuthService(db)

    try:
        payload = jwt.decode(
            token,
            auth_service.secret_key,
            algorithms=[auth_service.algorithm]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = auth_service.get_user(user_id)
    if user is None:
        raise credentials_exception

    if not user.ativo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo"
        )

    return user


async def get_current_active_user(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    """
    Retorna o usuário atual se estiver ativo.

    Args:
        current_user: Usuário atual

    Returns:
        Usuario: Usuário ativo

    Raises:
        HTTPException: Se o usuário estiver inativo
    """
    if not current_user.ativo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário inativo"
        )
    return current_user 