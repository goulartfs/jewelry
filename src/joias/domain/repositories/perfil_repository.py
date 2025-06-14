"""
Interface do repositório de Perfil.
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.perfil import Perfil


class IPerfilRepository(ABC):
    """Interface para o repositório de Perfil."""

    @abstractmethod
    def criar(self, perfil: Perfil) -> Perfil:
        """
        Cria um novo perfil.

        Args:
            perfil: Perfil a ser criado

        Returns:
            Perfil criado com ID
        """
        pass

    @abstractmethod
    def buscar_por_id(self, id: str) -> Optional[Perfil]:
        """
        Busca um perfil pelo ID.

        Args:
            id: ID do perfil

        Returns:
            Perfil encontrado ou None
        """
        pass

    @abstractmethod
    def buscar_por_nome(self, nome: str) -> Optional[Perfil]:
        """
        Busca um perfil pelo nome.

        Args:
            nome: Nome do perfil

        Returns:
            Perfil encontrado ou None
        """
        pass

    @abstractmethod
    def listar(self) -> List[Perfil]:
        """
        Lista todos os perfis.

        Returns:
            Lista de perfis
        """
        pass

    @abstractmethod
    def atualizar(self, perfil: Perfil) -> Perfil:
        """
        Atualiza um perfil existente.

        Args:
            perfil: Perfil com as alterações

        Returns:
            Perfil atualizado
        """
        pass

    @abstractmethod
    def deletar(self, perfil: Perfil) -> None:
        """
        Remove um perfil.

        Args:
            perfil: Perfil a ser removido
        """
        pass 