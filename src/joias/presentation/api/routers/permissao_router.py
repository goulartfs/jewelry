"""
Router para endpoints de Permissão.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from ....application.dtos.permissao import CriarPermissaoDTO, PermissaoDTO, AtualizarPermissaoDTO
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


@router.put(
    "/{id}",
    response_model=PermissaoDTO,
    description="Atualiza uma permissão existente",
)
def atualizar_permissao(
    id: str,
    dados: AtualizarPermissaoDTO,
    permissao_repository: IPermissaoRepository = Depends(get_permissao_repository),
) -> PermissaoDTO:
    """
    Atualiza uma permissão existente.

    Args:
        id: ID da permissão
        dados: Dados da permissão a serem atualizados
        permissao_repository: Repositório de permissões (injetado)

    Returns:
        Dados da permissão atualizada

    Raises:
        HTTPException: Se a permissão não for encontrada ou houver erro de validação
    """
    try:
        service = PermissaoService(permissao_repository)
        return service.atualizar_permissao(id, dados)
    except ValueError as e:
        raise HTTPException(status_code=404 if "não encontrada" in str(e) else 400, detail=str(e))


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Exclui uma permissão",
)
def excluir_permissao(
    id: str,
    permissao_repository: IPermissaoRepository = Depends(get_permissao_repository),
) -> None:
    """
    Exclui uma permissão do sistema.

    Args:
        id: ID da permissão
        permissao_repository: Repositório de permissões (injetado)

    Raises:
        HTTPException: Se a permissão não for encontrada ou não puder ser excluída
    """
    try:
        service = PermissaoService(permissao_repository)
        service.excluir_permissao(id)
    except ValueError as e:
        if "não encontrada" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=409, detail=str(e)) 