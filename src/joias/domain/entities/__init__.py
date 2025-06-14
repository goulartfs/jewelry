"""
Entidades do domínio.

Este módulo contém as entidades principais do domínio de negócio,
que são objetos que têm uma identidade única e são distinguíveis
mesmo quando seus atributos são idênticos.
"""

from .usuario import Usuario
from .contato import Contato
from .dados_pessoais import DadoPessoal
from .endereco import Endereco
from .empresa import Empresa
from .produto import Produto, Variacao, Detalhe, Preco
from .pedido import Pedido, ItemPedido
from .catalogo import Catalogo
from .autorizacao import Permissao, Perfil

__all__ = [
    'Usuario',
    'Contato',
    'DadoPessoal',
    'Endereco',
    'Empresa',
    'Produto',
    'Variacao',
    'Detalhe',
    'Preco',
    'Pedido',
    'ItemPedido',
    'Catalogo',
    'Permissao',
    'Perfil',
] 