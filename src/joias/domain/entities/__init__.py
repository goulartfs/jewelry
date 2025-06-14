"""
Entidades do domínio.

Este módulo contém as entidades principais do domínio de negócio,
que são objetos que têm uma identidade única e são distinguíveis
mesmo quando seus atributos são idênticos.
"""

from .autorizacao import Perfil, Permissao
from .catalogo import Catalogo
from .contato import Contato
from .dados_pessoais import DadoPessoal
from .empresa import Empresa
from .endereco import Endereco
from .pedido import ItemPedido, Pedido
from .produto import Detalhe, Preco, Produto, Variacao
from .usuario import Usuario

__all__ = [
    "Usuario",
    "Contato",
    "DadoPessoal",
    "Endereco",
    "Empresa",
    "Produto",
    "Variacao",
    "Detalhe",
    "Preco",
    "Pedido",
    "ItemPedido",
    "Catalogo",
    "Permissao",
    "Perfil",
]
