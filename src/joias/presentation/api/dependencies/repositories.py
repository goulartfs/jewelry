"""
Dependências para injeção de repositórios.

Este módulo fornece as funções de fábrica para injeção
de dependência dos repositórios na API.
"""
from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from ....domain.identity.repositories.usuario_repository import IUsuarioRepository
from ....infrastructure.persistence.sqlalchemy.repositories.usuario_repository import SQLUsuarioRepository
from ....infrastructure.persistence.sqlalchemy.session import get_db


def get_usuario_repository(
    db: Session = Depends(get_db)
) -> Generator[IUsuarioRepository, None, None]:
    """
    Retorna uma instância do repositório de usuários.
    
    Esta função é usada para injeção de dependência do
    repositório de usuários nos endpoints da API.
    
    Args:
        db: Sessão do banco de dados (injetada)
        
    Returns:
        Uma instância do repositório de usuários
    """
    try:
        repository = SQLUsuarioRepository(db)
        yield repository
    finally:
        db.close() 