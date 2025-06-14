"""
Router de usuários.

Este módulo implementa as rotas de usuários da API,
incluindo CRUD e operações específicas.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ....infrastructure.persistence.sqlalchemy.session import get_db
from ....application.identity.user_service import UserService
from ....domain.identity.entities.usuario import Usuario
from ....domain.shared.value_objects.email import Email
from ..schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserList
)
from ..dependencies.auth import get_current_user

router = APIRouter()


@router.post("/users", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    """
    Cria um novo usuário.

    Args:
        user: Dados do usuário a ser criado
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        Usuario: Usuário criado

    Raises:
        HTTPException: Se houver erro na criação
    """
    user_service = UserService(db)
    
    try:
        email = Email(user.email)
        created_user = user_service.create_user(
            email=email,
            nome=user.nome,
            senha=user.senha,
            empresa_id=current_user.empresa_id
        )
        return created_user
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/users", response_model=UserList)
async def list_users(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> List[Usuario]:
    """
    Lista usuários.

    Args:
        skip: Número de registros para pular
        limit: Número máximo de registros
        search: Termo de busca
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        List[Usuario]: Lista de usuários
    """
    user_service = UserService(db)
    return user_service.list_users(
        empresa_id=current_user.empresa_id,
        skip=skip,
        limit=limit,
        search=search
    )


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    """
    Busca um usuário pelo ID.

    Args:
        user_id: ID do usuário
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        Usuario: Usuário encontrado

    Raises:
        HTTPException: Se o usuário não for encontrado
    """
    user_service = UserService(db)
    user = user_service.get_user(user_id)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    if user.empresa_id != current_user.empresa_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado"
        )
    
    return user


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    """
    Atualiza um usuário.

    Args:
        user_id: ID do usuário
        user: Dados do usuário
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        Usuario: Usuário atualizado

    Raises:
        HTTPException: Se houver erro na atualização
    """
    user_service = UserService(db)
    existing_user = user_service.get_user(user_id)
    
    if existing_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    if existing_user.empresa_id != current_user.empresa_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado"
        )
    
    try:
        email = Email(user.email) if user.email else None
        updated_user = user_service.update_user(
            user_id=user_id,
            email=email,
            nome=user.nome,
            senha=user.senha
        )
        return updated_user
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> dict:
    """
    Remove um usuário.

    Args:
        user_id: ID do usuário
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        dict: Mensagem de sucesso

    Raises:
        HTTPException: Se houver erro na remoção
    """
    user_service = UserService(db)
    existing_user = user_service.get_user(user_id)
    
    if existing_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    if existing_user.empresa_id != current_user.empresa_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado"
        )
    
    user_service.delete_user(user_id)
    return {"message": "Usuário removido com sucesso"} 