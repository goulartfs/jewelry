"""
Interface base para repositórios.

Este módulo contém a interface base que todos os repositórios devem implementar.
"""
from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

from ..entities.base import Entity

T = TypeVar("T", bound=Entity)


class Repository(Generic[T], ABC):
    """
    Interface base para repositórios.

    Define o contrato que todos os repositórios devem seguir para
    persistir e recuperar entidades do domínio.
    """

    @abstractmethod
    def save(self, entity: T) -> T:
        """
        Salva uma entidade.

        Args:
            entity: Entidade a ser salva

        Returns:
            A entidade salva
        """
        pass

    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[T]:
        """
        Busca uma entidade pelo ID.

        Args:
            entity_id: ID da entidade

        Returns:
            A entidade encontrada ou None
        """
        pass

    @abstractmethod
    def list(self, active_only: bool = True) -> List[T]:
        """
        Lista todas as entidades.

        Args:
            active_only: Se True, retorna apenas entidades ativas

        Returns:
            Lista de entidades
        """
        pass

    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        """
        Remove uma entidade.

        Args:
            entity_id: ID da entidade

        Returns:
            True se removida com sucesso, False caso contrário
        """
        pass

    @abstractmethod
    def update(self, entity: T) -> Optional[T]:
        """
        Atualiza uma entidade.

        Args:
            entity: Entidade com dados atualizados

        Returns:
            A entidade atualizada ou None se não encontrada
        """
        pass
