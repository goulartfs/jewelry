"""
Interface para repositório de usuários.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ..entities.usuario import Usuario
from ..shared.value_objects import Email


class IUsuarioRepository(ABC):
    """
    Interface para repositório de usuários.
    """

    @abstractmethod
    def criar(self, usuario: Usuario) -> Usuario:
        """
        Cria um novo usuário.

        Args:
            usuario: Usuário a ser criado

        Returns:
            Usuário criado
        """
        pass

    @abstractmethod
    def buscar_por_id(self, id: str) -> Optional[Usuario]:
        """
        Busca um usuário pelo ID.

        Args:
            id: ID do usuário

        Returns:
            Usuário encontrado ou None
        """
        pass

    @abstractmethod
    def buscar_por_email(self, email: Email) -> Optional[Usuario]:
        """
        Busca um usuário pelo email.

        Args:
            email: Email do usuário

        Returns:
            Usuário encontrado ou None
        """
        pass

    @abstractmethod
    def listar(self) -> List[Usuario]:
        """
        Lista todos os usuários.

        Returns:
            Lista de usuários
        """
        pass

    @abstractmethod
    def atualizar(self, usuario: Usuario) -> Usuario:
        """
        Atualiza um usuário.

        Args:
            usuario: Usuário a ser atualizado

        Returns:
            Usuário atualizado
        """
        pass

    @abstractmethod
    def excluir(self, usuario: Usuario) -> None:
        """
        Exclui um usuário.

        Args:
            usuario: Usuário a ser excluído
        """
        pass 