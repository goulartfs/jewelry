"""
Sistema de Joias.

Este é o pacote principal do sistema de joias, que contém todos os módulos
e funcionalidades necessários para gerenciar um negócio de joias.
"""

from .domain import *

__all__ = [
    # Re-export everything from domain module
    'Usuario', 'Contato', 'DadoPessoal', 'Endereco', 'Empresa',
    'Permissao', 'Perfil', 'Produto', 'Catalogo', 'Pedido', 'ItemPedido',
    'Preco', 'Detalhe', 'Variacao',
    'BaseService', 'UsuarioService', 'ContatoService', 'DadoPessoalService',
    'EmpresaService', 'PermissaoService', 'PerfilService', 'ProdutoService',
    'CatalogoService', 'PedidoService'
] 