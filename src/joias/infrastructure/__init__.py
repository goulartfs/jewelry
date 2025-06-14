"""
Pacote de infraestrutura.

Este pacote contém a camada de infraestrutura do sistema,
implementando detalhes técnicos como persistência e mensageria.
"""

from .config import Settings, get_settings
from .database import Database, get_database
from .persistence.sqlalchemy.models import Base
from .persistence.sqlalchemy.session import get_db
from .repositories import (
    CatalogoRepository,
    InMemoryRepository,
    PedidoRepository,
    ProdutoRepository,
    SQLAlchemyRepository,
    UsuarioRepository,
)

__all__ = [
    # Repositórios
    "InMemoryRepository",
    "SQLAlchemyRepository",
    "UsuarioRepository",
    "ProdutoRepository",
    "PedidoRepository",
    "CatalogoRepository",
    # Database
    "Database",
    "get_database",
    # Configurações
    "Settings",
    "get_settings",
    "get_db",
    "Base",
]
