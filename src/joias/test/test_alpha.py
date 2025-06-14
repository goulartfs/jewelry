"""
Testes para o módulo alpha.

Este módulo contém os testes unitários para as entidades e serviços do módulo alpha.
"""
import unittest
from datetime import datetime
from decimal import Decimal
from joias.domain.alpha import (
    Usuario, Contato, DadoPessoal, Endereco, Empresa,
    Permissao, Perfil, Produto, Catalogo, Pedido, ItemPedido,
    Preco, Detalhe, Variacao,
    UsuarioService, ContatoService, DadoPessoalService,
    EmpresaService, PermissaoService, PerfilService,
    ProdutoService, CatalogoService, PedidoService
)

# ... rest of the existing code ... 