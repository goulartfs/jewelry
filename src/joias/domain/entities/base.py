"""
Classes base para entidades do domínio.

Este módulo contém as classes base que todas as entidades do domínio devem herdar.
"""
from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Entity(ABC):
    """
    Classe base para todas as entidades do domínio.

    Uma entidade é um objeto que tem uma identidade única e é distinguível
    mesmo quando seus atributos são idênticos.
    """

    id: int
    data_criacao: datetime = field(default_factory=datetime.now)
    data_atualizacao: Optional[datetime] = None
    ativo: bool = True

    def __eq__(self, other):
        if not isinstance(other, Entity):
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def atualizar(self) -> None:
        """Atualiza a data de atualização da entidade."""
        self.data_atualizacao = datetime.now()

    def desativar(self) -> None:
        """Desativa a entidade."""
        self.ativo = False
        self.atualizar()

    def ativar(self) -> None:
        """Ativa a entidade."""
        self.ativo = True
        self.atualizar()
