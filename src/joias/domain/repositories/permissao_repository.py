"""
Interface do repositório de Permissão.
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.permissao import Permissao


class IPermissaoRepository(ABC):
    """Interface para o repositório de Permissão."""

    @abstractmethod
    def criar(self, permissao: Permissao) -> Permissao:
        """
        Cria uma nova permissão.

        Args:
            permissao: Permissão a ser criada

        Returns:
            Permissão criada com ID
        """
        pass

    @abstractmethod
    def buscar_por_id(self, id: str) -> Optional[Permissao]:
        """
        Busca uma permissão pelo ID.

        Args:
            id: ID da permissão

        Returns:
            Permissão encontrada ou None
        """
        pass

    @abstractmethod
    def buscar_por_chave(self, chave: str) -> Optional[Permissao]:
        """
        Busca uma permissão pela chave.

        Args:
            chave: Chave da permissão

        Returns:
            Permissão encontrada ou None
        """
        pass

    @abstractmethod
    def listar(self) -> List[Permissao]:
        """
        Lista todas as permissões.

        Returns:
            Lista de permissões
        """
        pass

    @abstractmethod
    def deletar(self, permissao: Permissao) -> None:
        """
        Remove uma permissão.

        Args:
            permissao: Permissão a ser removida
        """
        pass 