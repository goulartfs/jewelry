"""
Repositórios do domínio.

Este módulo contém as interfaces dos repositórios que definem
como as entidades do domínio são persistidas e recuperadas.
"""

from .base import Repository
from .usuario import UsuarioRepository
from .produto import ProdutoRepository
from .pedido import PedidoRepository
from .catalogo import CatalogoRepository

__all__ = [
    'Repository',
    'UsuarioRepository',
    'ProdutoRepository',
    'PedidoRepository',
    'CatalogoRepository',
] 