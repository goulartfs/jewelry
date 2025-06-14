"""
Módulo alpha do sistema de joias.

Este módulo contém as entidades e serviços principais do sistema,
incluindo usuários, contatos, dados pessoais, endereços, etc.
"""

from .models import (
    Catalogo,
    Contato,
    DadoPessoal,
    Detalhe,
    Empresa,
    Endereco,
    ItemPedido,
    Pedido,
    Perfil,
    Permissao,
    Preco,
    Produto,
    Usuario,
    Variacao,
)
from .service import (
    BaseService,
    CatalogoService,
    ContatoService,
    DadoPessoalService,
    EmpresaService,
    PedidoService,
    PerfilService,
    PermissaoService,
    ProdutoService,
    UsuarioService,
)

__all__ = [
    "Usuario",
    "Contato",
    "DadoPessoal",
    "Endereco",
    "Empresa",
    "Permissao",
    "Perfil",
    "Produto",
    "Catalogo",
    "Pedido",
    "ItemPedido",
    "Preco",
    "Detalhe",
    "Variacao",
    "BaseService",
    "UsuarioService",
    "ContatoService",
    "DadoPessoalService",
    "EmpresaService",
    "PermissaoService",
    "PerfilService",
    "ProdutoService",
    "CatalogoService",
    "PedidoService",
]
