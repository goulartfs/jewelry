"""
Casos de uso da aplicação.

Este módulo contém os casos de uso que implementam as regras de negócio
da aplicação, orquestrando as entidades do domínio e seus repositórios.
"""

from .usuario import (
    CriarUsuarioUseCase,
    AtualizarUsuarioUseCase,
    BuscarUsuarioUseCase,
    ListarUsuariosUseCase,
    RemoverUsuarioUseCase
)

from .produto import (
    CriarProdutoUseCase,
    AtualizarProdutoUseCase,
    BuscarProdutoUseCase,
    ListarProdutosUseCase,
    RemoverProdutoUseCase,
    AdicionarVariacaoUseCase,
    AdicionarDetalheUseCase
)

from .pedido import (
    CriarPedidoUseCase,
    AdicionarItemPedidoUseCase,
    ConfirmarPedidoUseCase,
    CancelarPedidoUseCase,
    BuscarPedidoUseCase,
    ListarPedidosUseCase
)

from .catalogo import (
    CriarCatalogoUseCase,
    AtualizarCatalogoUseCase,
    BuscarCatalogoUseCase,
    ListarCatalogosUseCase,
    AdicionarProdutoCatalogoUseCase
)

__all__ = [
    # Usuário
    'CriarUsuarioUseCase',
    'AtualizarUsuarioUseCase',
    'BuscarUsuarioUseCase',
    'ListarUsuariosUseCase',
    'RemoverUsuarioUseCase',
    # Produto
    'CriarProdutoUseCase',
    'AtualizarProdutoUseCase',
    'BuscarProdutoUseCase',
    'ListarProdutosUseCase',
    'RemoverProdutoUseCase',
    'AdicionarVariacaoUseCase',
    'AdicionarDetalheUseCase',
    # Pedido
    'CriarPedidoUseCase',
    'AdicionarItemPedidoUseCase',
    'ConfirmarPedidoUseCase',
    'CancelarPedidoUseCase',
    'BuscarPedidoUseCase',
    'ListarPedidosUseCase',
    # Catálogo
    'CriarCatalogoUseCase',
    'AtualizarCatalogoUseCase',
    'BuscarCatalogoUseCase',
    'ListarCatalogosUseCase',
    'AdicionarProdutoCatalogoUseCase',
] 