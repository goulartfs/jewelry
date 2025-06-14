"""
Pacote de repositórios SQLAlchemy.

Este pacote contém as implementações dos repositórios
usando SQLAlchemy como mecanismo de persistência.
"""
from .usuario_repository import UsuarioRepository

__all__ = [
    'UsuarioRepository'
] 