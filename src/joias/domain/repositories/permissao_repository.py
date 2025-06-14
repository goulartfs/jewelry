"""
Interface para repositório de permissões.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ..entities.permissao import Permissao


class IPermissaoRepository(ABC):
    """
    Interface para repositório de permissões.
    """

    @abstractmethod
    def criar(self, permissao: Permissao) -> Permissao:
        """
        Cria uma nova permissão.

        Args:
            permissao: Permissão a ser criada

        Returns:
            Permissão criada
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
    def atualizar(self, permissao: Permissao) -> Permissao:
        """
        Atualiza uma permissão.

        Args:
            permissao: Permissão a ser atualizada

        Returns:
            Permissão atualizada
        """
        pass

    @abstractmethod
    def excluir(self, permissao: Permissao) -> None:
        """
        Exclui uma permissão.

        Args:
            permissao: Permissão a ser excluída
        """
        pass

    @abstractmethod
    def tem_perfis_associados(self, id: UUID) -> bool:
        """
        Verifica se uma permissão está associada a algum perfil.

        Args:
            id: ID da permissão

        Returns:
            True se a permissão estiver associada a algum perfil, False caso contrário
        """
        pass 