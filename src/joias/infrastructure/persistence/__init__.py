"""
Pacote de persistência.

Este pacote contém as implementações de persistência do sistema,
incluindo SQLAlchemy e outros mecanismos de armazenamento.
"""
from .sqlalchemy.models import Base
from .sqlalchemy.repositories.usuario_repository import UsuarioRepository
from .sqlalchemy.session import get_db

__all__ = ["get_db", "Base", "UsuarioRepository"]
