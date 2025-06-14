"""
Pacote raiz do sistema de joias.

Este pacote contém o módulo principal do sistema de joias e todos os seus subpacotes.
"""

from .joias import *

__all__ = [
    # Re-export everything from joias module
    'Usuario', 'Contato', 'DadoPessoal', 'Endereco', 'Empresa',
    'Permissao', 'Perfil', 'Produto', 'Catalogo', 'Pedido', 'ItemPedido',
    'Preco', 'Detalhe', 'Variacao',
    'BaseService', 'UsuarioService', 'ContatoService', 'DadoPessoalService',
    'EmpresaService', 'PermissaoService', 'PerfilService', 'ProdutoService',
    'CatalogoService', 'PedidoService'
] 