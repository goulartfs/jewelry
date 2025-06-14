"""
Pacote de infraestrutura.

Este pacote contém a camada de infraestrutura do sistema,
implementando detalhes técnicos como persistência e mensageria.
"""

from .repositories import (
    InMemoryRepository,
    SQLAlchemyRepository,
    UsuarioRepository,
    ProdutoRepository,
    PedidoRepository,
    CatalogoRepository
)

from .database import Database, get_database
from .config import Settings, get_settings
from .persistence.sqlalchemy.session import get_db
from .persistence.sqlalchemy.models import Base

__all__ = [
    # Repositórios
    'InMemoryRepository',
    'SQLAlchemyRepository',
    'UsuarioRepository',
    'ProdutoRepository',
    'PedidoRepository',
    'CatalogoRepository',
    # Database
    'Database',
    'get_database',
    # Configurações
    'Settings',
    'get_settings',
    'get_db',
    'Base',
] 