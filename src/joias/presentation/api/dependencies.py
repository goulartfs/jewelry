"""
Dependências da API.

Este módulo contém as funções de injeção de dependência
utilizadas pelos endpoints da API.
"""
from fastapi import Depends
from sqlalchemy.orm import Session

from ...domain.repositories.perfil_repository import IPerfilRepository
from ...domain.repositories.permissao_repository import IPermissaoRepository
from ...infrastructure.persistence.sqlalchemy.repositories.perfil_repository import (
    SQLPerfilRepository,
)
from ...infrastructure.persistence.sqlalchemy.repositories.permissao_repository import (
    SQLPermissaoRepository,
)
from ...infrastructure.persistence.sqlalchemy.session import get_session


def get_permissao_repository(
    session: Session = Depends(get_session),
) -> IPermissaoRepository:
    """
    Retorna uma instância do repositório de permissões.

    Args:
        session: Sessão do SQLAlchemy (injetada)

    Returns:
        Repositório de permissões
    """
    return SQLPermissaoRepository(session)


def get_perfil_repository(
    session: Session = Depends(get_session),
) -> IPerfilRepository:
    """
    Retorna uma instância do repositório de perfis.

    Args:
        session: Sessão do SQLAlchemy (injetada)

    Returns:
        Repositório de perfis
    """
    return SQLPerfilRepository(session) 