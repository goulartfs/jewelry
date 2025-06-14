"""
Entidades de autorização.

Este módulo contém as entidades relacionadas à autorização de usuários,
como permissões e perfis.
"""
from dataclasses import dataclass, field
from typing import List

from .base import Entity


@dataclass
class Permissao(Entity):
    """
    Entidade que representa uma permissão no sistema.

    Uma permissão define uma ação específica que pode ser executada
    por um usuário que possui essa permissão através de seu perfil.
    """

    nome: str
    descricao: str
    codigo: str

    def __eq__(self, other):
        if not isinstance(other, Permissao):
            return NotImplemented
        return self.codigo == other.codigo

    def __hash__(self):
        return hash(self.codigo)


@dataclass
class Perfil(Entity):
    """
    Entidade que representa um perfil de usuário.

    Um perfil é um conjunto de permissões que define o que um
    usuário pode ou não fazer no sistema.
    """

    nome: str
    descricao: str
    permissoes: List[Permissao] = field(default_factory=list)

    def adicionar_permissao(self, permissao: Permissao) -> None:
        """
        Adiciona uma permissão ao perfil.

        Args:
            permissao: Permissão a ser adicionada
        """
        if permissao not in self.permissoes:
            self.permissoes.append(permissao)
            self.atualizar()

    def remover_permissao(self, permissao: Permissao) -> None:
        """
        Remove uma permissão do perfil.

        Args:
            permissao: Permissão a ser removida
        """
        if permissao in self.permissoes:
            self.permissoes.remove(permissao)
            self.atualizar()

    def tem_permissao(self, codigo_permissao: str) -> bool:
        """
        Verifica se o perfil tem uma determinada permissão.

        Args:
            codigo_permissao: Código da permissão a ser verificada

        Returns:
            True se o perfil tem a permissão, False caso contrário
        """
        return any(p.codigo == codigo_permissao for p in self.permissoes)
