"""
Interface base para repositórios.

Este módulo define a interface base que todos os repositórios devem
implementar, seguindo os princípios do Domain-Driven Design.
"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List
from uuid import UUID

from ..entities.aggregate_root import AggregateRoot

T = TypeVar('T', bound=AggregateRoot)


class Repository(Generic[T], ABC):
    """
    Interface base para repositórios.

    Esta interface define os métodos básicos que todo repositório
    deve implementar para persistir e recuperar agregados.

    Args:
        T: Tipo do agregado gerenciado pelo repositório
    """

    @abstractmethod
    def proximo_id(self) -> UUID:
        """
        Gera o próximo ID para uma nova entidade.

        Returns:
            UUID: Novo identificador único
        """
        pass

    @abstractmethod
    def salvar(self, agregado: T) -> T:
        """
        Persiste um agregado no repositório.

        Args:
            agregado: O agregado a ser salvo

        Returns:
            T: O agregado salvo

        Raises:
            ValueError: Se houver erro de validação
            VersionError: Se houver conflito de versão
        """
        pass

    @abstractmethod
    def buscar_por_id(self, id: UUID) -> Optional[T]:
        """
        Busca um agregado pelo seu ID.

        Args:
            id: ID do agregado

        Returns:
            Optional[T]: O agregado encontrado ou None
        """
        pass

    @abstractmethod
    def listar(self, apenas_ativos: bool = True) -> List[T]:
        """
        Lista todos os agregados.

        Args:
            apenas_ativos: Se True, retorna apenas agregados ativos

        Returns:
            List[T]: Lista de agregados
        """
        pass

    @abstractmethod
    def excluir(self, id: UUID) -> bool:
        """
        Remove um agregado do repositório.

        Args:
            id: ID do agregado

        Returns:
            bool: True se removido com sucesso, False caso contrário
        """
        pass 