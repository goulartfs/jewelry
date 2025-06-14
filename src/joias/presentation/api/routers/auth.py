"""
Router de autenticação.

Este módulo implementa as rotas de autenticação da API,
incluindo login, logout e refresh token.
"""
from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from ....application.identity.auth_service import AuthService
from ....domain.identity.entities.usuario import Usuario
from ....domain.shared.value_objects.email import Email
from ....infrastructure.persistence.sqlalchemy.session import get_db

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/auth/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> dict:
    """
    Autentica um usuário e retorna um token de acesso.

    Args:
        form_data: Dados do formulário de login
        db: Sessão do banco de dados

    Returns:
        dict: Token de acesso e tipo do token

    Raises:
        HTTPException: Se as credenciais forem inválidas
    """
    auth_service = AuthService(db)

    try:
        email = Email(form_data.username)
        user = auth_service.authenticate(email, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = auth_service.create_access_token(
            data={"sub": str(user.id)}, expires_delta=timedelta(minutes=30)
        )

        return {"access_token": access_token, "token_type": "bearer"}

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/auth/refresh")
async def refresh_token(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> dict:
    """
    Atualiza um token de acesso.

    Args:
        token: Token de acesso atual
        db: Sessão do banco de dados

    Returns:
        dict: Novo token de acesso e tipo do token

    Raises:
        HTTPException: Se o token for inválido
    """
    auth_service = AuthService(db)

    try:
        payload = jwt.decode(
            token, auth_service.secret_key, algorithms=[auth_service.algorithm]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = auth_service.create_access_token(
            data={"sub": user_id}, expires_delta=timedelta(minutes=30)
        )

        return {"access_token": access_token, "token_type": "bearer"}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/auth/me")
async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> Usuario:
    """
    Retorna o usuário atual.

    Args:
        token: Token de acesso
        db: Sessão do banco de dados

    Returns:
        Usuario: Usuário atual

    Raises:
        HTTPException: Se o token for inválido
    """
    auth_service = AuthService(db)

    try:
        payload = jwt.decode(
            token, auth_service.secret_key, algorithms=[auth_service.algorithm]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = auth_service.get_user(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário não encontrado",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
