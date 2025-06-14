"""
Rotas da API para gerenciamento de usuários.

Este módulo implementa os endpoints REST para operações
relacionadas a usuários.
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, EmailStr

from ....application.identity.user_service import (
    CriarUsuarioDTO,
    UserService,
    UsuarioDTO,
)
from ....domain.identity.repositories.usuario_repository import IUsuarioRepository
from ..dependencies.repositories import get_usuario_repository

router = APIRouter(prefix="/api/usuarios", tags=["Usuários"])


class CriarUsuarioRequest(BaseModel):
    """Schema para requisição de criação de usuário."""

    nome: str
    email: EmailStr
    senha: str

    class Config:
        json_schema_extra = {
            "example": {
                "nome": "João da Silva",
                "email": "joao@email.com",
                "senha": "senha123",
            }
        }


@router.post(
    "",
    response_model=UsuarioDTO,
    status_code=201,
    description="Cria um novo usuário no sistema",
)
def criar_usuario(
    dados: CriarUsuarioRequest,
    repository: IUsuarioRepository = Depends(get_usuario_repository),
) -> UsuarioDTO:
    """
    Cria um novo usuário no sistema.

    Este endpoint implementa o caso de uso US1, permitindo o cadastro
    de novos usuários com nome, email e senha.

    Args:
        dados: Dados do usuário a ser criado
        repository: Repositório de usuários (injetado)

    Returns:
        Dados do usuário criado

    Raises:
        HTTPException: Se houver erro de validação ou conflito
    """
    try:
        service = UserService(repository)
        return service.criar_usuario(
            CriarUsuarioDTO(nome=dados.nome, email=dados.email, senha=dados.senha)
        )
    except ValueError as e:
        if "já cadastrado" in str(e):
            raise HTTPException(status_code=409, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/{id}",
    response_model=UsuarioDTO,
    description="Retorna os dados de um usuário específico",
)
def buscar_usuario(
    id: str, repository: IUsuarioRepository = Depends(get_usuario_repository)
) -> UsuarioDTO:
    """
    Busca um usuário pelo ID.

    Args:
        id: ID do usuário
        repository: Repositório de usuários (injetado)

    Returns:
        Dados do usuário

    Raises:
        HTTPException: Se o usuário não for encontrado
    """
    service = UserService(repository)
    usuario = service.buscar_usuario(id)

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return usuario


@router.get(
    "",
    response_model=List[UsuarioDTO],
    description="Lista usuários com paginação e filtros",
)
def listar_usuarios(
    pagina: int = Query(1, ge=1, description="Número da página"),
    tamanho: int = Query(10, ge=1, le=100, description="Tamanho da página"),
    email: Optional[str] = Query(None, description="Filtro por email"),
    nome: Optional[str] = Query(None, description="Filtro por nome"),
    repository: IUsuarioRepository = Depends(get_usuario_repository),
) -> List[UsuarioDTO]:
    """
    Lista usuários com paginação e filtros opcionais.

    Args:
        pagina: Número da página
        tamanho: Tamanho da página
        email: Filtro por email
        nome: Filtro por nome
        repository: Repositório de usuários (injetado)

    Returns:
        Lista de usuários
    """
    service = UserService(repository)
    return service.listar_usuarios(
        pagina=pagina, tamanho=tamanho, email=email, nome=nome
    )
