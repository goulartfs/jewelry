"""
Repositórios do domínio.

Este módulo contém as interfaces dos repositórios que definem
como as entidades do domínio são persistidas e recuperadas.
"""

from .base import Repository
from .catalogo import CatalogoRepository
from .pedido import PedidoRepository
from .produto import ProdutoRepository
from .usuario import UsuarioRepository

__all__ = [
    "Repository",
    "UsuarioRepository",
    "ProdutoRepository",
    "PedidoRepository",
    "CatalogoRepository",
]
