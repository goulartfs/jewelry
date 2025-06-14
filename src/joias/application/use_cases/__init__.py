"""
Casos de uso da aplicação.

Este módulo contém os casos de uso que implementam as regras de negócio
da aplicação, orquestrando as entidades do domínio e seus repositórios.
"""

from .catalogo import (
    AdicionarProdutoCatalogoUseCase,
    AtualizarCatalogoUseCase,
    BuscarCatalogoUseCase,
    CriarCatalogoUseCase,
    ListarCatalogosUseCase,
)
from .pedido import (
    AdicionarItemPedidoUseCase,
    BuscarPedidoUseCase,
    CancelarPedidoUseCase,
    ConfirmarPedidoUseCase,
    CriarPedidoUseCase,
    ListarPedidosUseCase,
)
from .produto import (
    AdicionarDetalheUseCase,
    AdicionarVariacaoUseCase,
    AtualizarProdutoUseCase,
    BuscarProdutoUseCase,
    CriarProdutoUseCase,
    ListarProdutosUseCase,
    RemoverProdutoUseCase,
)
from .usuario import (
    AtualizarUsuarioUseCase,
    BuscarUsuarioUseCase,
    CriarUsuarioUseCase,
    ListarUsuariosUseCase,
    RemoverUsuarioUseCase,
)

__all__ = [
    # Usuário
    "CriarUsuarioUseCase",
    "AtualizarUsuarioUseCase",
    "BuscarUsuarioUseCase",
    "ListarUsuariosUseCase",
    "RemoverUsuarioUseCase",
    # Produto
    "CriarProdutoUseCase",
    "AtualizarProdutoUseCase",
    "BuscarProdutoUseCase",
    "ListarProdutosUseCase",
    "RemoverProdutoUseCase",
    "AdicionarVariacaoUseCase",
    "AdicionarDetalheUseCase",
    # Pedido
    "CriarPedidoUseCase",
    "AdicionarItemPedidoUseCase",
    "ConfirmarPedidoUseCase",
    "CancelarPedidoUseCase",
    "BuscarPedidoUseCase",
    "ListarPedidosUseCase",
    # Catálogo
    "CriarCatalogoUseCase",
    "AtualizarCatalogoUseCase",
    "BuscarCatalogoUseCase",
    "ListarCatalogosUseCase",
    "AdicionarProdutoCatalogoUseCase",
]
