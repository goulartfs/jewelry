"""
Módulo alpha do sistema de joias.

Este módulo contém as entidades e serviços principais do sistema,
incluindo usuários, contatos, dados pessoais, endereços, etc.
"""

from .models import (
    Usuario, Contato, DadoPessoal, Endereco, Empresa,
    Permissao, Perfil, Produto, Catalogo, Pedido, ItemPedido,
    Preco, Detalhe, Variacao
)

from .service import (
    BaseService, UsuarioService, ContatoService, DadoPessoalService,
    EmpresaService, PermissaoService, PerfilService, ProdutoService,
    CatalogoService, PedidoService
)

__all__ = [
    'Usuario', 'Contato', 'DadoPessoal', 'Endereco', 'Empresa',
    'Permissao', 'Perfil', 'Produto', 'Catalogo', 'Pedido', 'ItemPedido',
    'Preco', 'Detalhe', 'Variacao',
    'BaseService', 'UsuarioService', 'ContatoService', 'DadoPessoalService',
    'EmpresaService', 'PermissaoService', 'PerfilService', 'ProdutoService',
    'CatalogoService', 'PedidoService'
] 