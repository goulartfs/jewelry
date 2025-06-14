"""
Pacote de entidades do domínio.

Este pacote contém todas as entidades do domínio,
organizadas por contexto.
"""
from .autorizacao import Perfil, Permissao, Usuario

__all__ = ["Perfil", "Permissao", "Usuario"]
