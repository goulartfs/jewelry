"""
Router para endpoints de Perfil.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from ....application.dtos.perfil import CriarPerfilDTO, PerfilDTO, AtualizarPerfilDTO
from ....application.identity.perfil_service import PerfilService
from ....domain.repositories.perfil_repository import IPerfilRepository
from ....domain.repositories.permissao_repository import IPermissaoRepository
from ...dependencies import get_perfil_repository, get_permissao_repository

router = APIRouter(prefix="/perfis", tags=["Perfis"])


@router.post(
    "",
    response_model=PerfilDTO,
    status_code=201,
    description="Cria um novo perfil",
)
def criar_perfil(
    dados: CriarPerfilDTO,
    perfil_repository: IPerfilRepository = Depends(get_perfil_repository),
    permissao_repository: IPermissaoRepository = Depends(get_permissao_repository),
) -> PerfilDTO:
    """
    Cria um novo perfil.

    Args:
        dados: Dados do perfil
        perfil_repository: Repositório de perfis (injetado)
        permissao_repository: Repositório de permissões (injetado)

    Returns:
        Dados do perfil criado

    Raises:
        HTTPException: Se houver erro de validação
    """
    try:
        service = PerfilService(perfil_repository, permissao_repository)
        return service.criar_perfil(dados)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/{id}",
    response_model=PerfilDTO,
    description="Retorna os dados de um perfil específico",
)
def buscar_perfil(
    id: str,
    perfil_repository: IPerfilRepository = Depends(get_perfil_repository),
    permissao_repository: IPermissaoRepository = Depends(get_permissao_repository),
) -> PerfilDTO:
    """
    Busca um perfil pelo ID.

    Args:
        id: ID do perfil
        perfil_repository: Repositório de perfis (injetado)
        permissao_repository: Repositório de permissões (injetado)

    Returns:
        Dados do perfil

    Raises:
        HTTPException: Se o perfil não for encontrado
    """
    service = PerfilService(perfil_repository, permissao_repository)
    perfil = service.buscar_perfil(id)

    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil não encontrado")

    return perfil


@router.get(
    "",
    response_model=List[PerfilDTO],
    description="Lista todos os perfis",
)
def listar_perfis(
    perfil_repository: IPerfilRepository = Depends(get_perfil_repository),
    permissao_repository: IPermissaoRepository = Depends(get_permissao_repository),
) -> List[PerfilDTO]:
    """
    Lista todos os perfis.

    Args:
        perfil_repository: Repositório de perfis (injetado)
        permissao_repository: Repositório de permissões (injetado)

    Returns:
        Lista de perfis
    """
    service = PerfilService(perfil_repository, permissao_repository)
    return service.listar_perfis()


@router.post(
    "/{perfil_id}/permissoes/{permissao_id}",
    response_model=PerfilDTO,
    description="Adiciona uma permissão a um perfil",
)
def adicionar_permissao(
    perfil_id: str,
    permissao_id: str,
    perfil_repository: IPerfilRepository = Depends(get_perfil_repository),
    permissao_repository: IPermissaoRepository = Depends(get_permissao_repository),
) -> PerfilDTO:
    """
    Adiciona uma permissão a um perfil.

    Args:
        perfil_id: ID do perfil
        permissao_id: ID da permissão
        perfil_repository: Repositório de perfis (injetado)
        permissao_repository: Repositório de permissões (injetado)

    Returns:
        Dados do perfil atualizado

    Raises:
        HTTPException: Se o perfil ou a permissão não forem encontrados
    """
    try:
        service = PerfilService(perfil_repository, permissao_repository)
        return service.adicionar_permissao(perfil_id, permissao_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete(
    "/{perfil_id}/permissoes/{permissao_id}",
    response_model=PerfilDTO,
    description="Remove uma permissão de um perfil",
)
def remover_permissao(
    perfil_id: str,
    permissao_id: str,
    perfil_repository: IPerfilRepository = Depends(get_perfil_repository),
    permissao_repository: IPermissaoRepository = Depends(get_permissao_repository),
) -> PerfilDTO:
    """
    Remove uma permissão de um perfil.

    Args:
        perfil_id: ID do perfil
        permissao_id: ID da permissão
        perfil_repository: Repositório de perfis (injetado)
        permissao_repository: Repositório de permissões (injetado)

    Returns:
        Dados do perfil atualizado

    Raises:
        HTTPException: Se o perfil ou a permissão não forem encontrados
    """
    try:
        service = PerfilService(perfil_repository, permissao_repository)
        return service.remover_permissao(perfil_id, permissao_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put(
    "/{id}",
    response_model=PerfilDTO,
    description="Atualiza um perfil existente",
)
def atualizar_perfil(
    id: str,
    dados: AtualizarPerfilDTO,
    perfil_repository: IPerfilRepository = Depends(get_perfil_repository),
    permissao_repository: IPermissaoRepository = Depends(get_permissao_repository),
) -> PerfilDTO:
    """
    Atualiza um perfil existente.

    Args:
        id: ID do perfil
        dados: Dados do perfil a serem atualizados
        perfil_repository: Repositório de perfis (injetado)
        permissao_repository: Repositório de permissões (injetado)

    Returns:
        Dados do perfil atualizado

    Raises:
        HTTPException: Se o perfil não for encontrado ou houver erro de validação
    """
    try:
        service = PerfilService(perfil_repository, permissao_repository)
        return service.atualizar_perfil(id, dados)
    except ValueError as e:
        raise HTTPException(status_code=404 if "não encontrado" in str(e) else 400, detail=str(e))


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Exclui um perfil",
)
def excluir_perfil(
    id: str,
    perfil_repository: IPerfilRepository = Depends(get_perfil_repository),
    permissao_repository: IPermissaoRepository = Depends(get_permissao_repository),
) -> None:
    """
    Exclui um perfil do sistema.

    Args:
        id: ID do perfil
        perfil_repository: Repositório de perfis (injetado)
        permissao_repository: Repositório de permissões (injetado)

    Raises:
        HTTPException: Se o perfil não for encontrado ou não puder ser excluído
    """
    try:
        service = PerfilService(perfil_repository, permissao_repository)
        service.excluir_perfil(id)
    except ValueError as e:
        if "não encontrado" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=409, detail=str(e)) 