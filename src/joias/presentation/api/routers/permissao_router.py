"""
Router para endpoints de Permissão.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from ....application.dtos.permissao import CriarPermissaoDTO, PermissaoDTO
from ....application.identity.permissao_service import PermissaoService
from ....domain.repositories.permissao_repository import IPermissaoRepository
from ...dependencies import get_permissao_repository

router = APIRouter(prefix="/permissoes", tags=["Permissões"])


@router.post(
    "",
    response_model=PermissaoDTO,
    status_code=status.HTTP_201_CREATED,
    description="Cria uma nova permissão",
)
def criar_permissao(
    dados: CriarPermissaoDTO,
    permissao_repository: IPermissaoRepository = Depends(get_permissao_repository),
) -> PermissaoDTO:
    """
    Cria uma nova permissão.

    Args:
        dados: Dados da permissão
        permissao_repository: Repositório de permissões (injetado)

    Returns:
        Dados da permissão criada

    Raises:
        HTTPException: Se houver erro de validação
    """
    try:
        service = PermissaoService(permissao_repository)
        return service.criar_permissao(dados)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/{id}",
    response_model=PermissaoDTO,
    description="Retorna os dados de uma permissão específica",
)
def buscar_permissao(
    id: str,
    permissao_repository: IPermissaoRepository = Depends(get_permissao_repository),
) -> PermissaoDTO:
    """
    Busca uma permissão pelo ID.

    Args:
        id: ID da permissão
        permissao_repository: Repositório de permissões (injetado)

    Returns:
        Dados da permissão

    Raises:
        HTTPException: Se a permissão não for encontrada
    """
    service = PermissaoService(permissao_repository)
    permissao = service.buscar_permissao(id)

    if not permissao:
        raise HTTPException(status_code=404, detail="Permissão não encontrada")

    return permissao


@router.get(
    "",
    response_model=List[PermissaoDTO],
    description="Lista todas as permissões",
)
def listar_permissoes(
    permissao_repository: IPermissaoRepository = Depends(get_permissao_repository),
) -> List[PermissaoDTO]:
    """
    Lista todas as permissões.

    Args:
        permissao_repository: Repositório de permissões (injetado)

    Returns:
        Lista de permissões
    """
    service = PermissaoService(permissao_repository)
    return service.listar_permissoes() 