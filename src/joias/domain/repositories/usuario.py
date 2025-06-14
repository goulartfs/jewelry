"""
Repositório de usuários.

Este módulo contém a interface do repositório de usuários
e suas implementações.
"""
from abc import abstractmethod
from typing import List, Optional

from ..entities.usuario import Usuario
from .base import Repository


class UsuarioRepository(Repository[Usuario]):
    """Interface do repositório de usuários."""

    @abstractmethod
    def buscar_por_username(self, username: str) -> Optional[Usuario]:
        """
        Busca um usuário pelo username.

        Args:
            username: Username do usuário

        Returns:
            O usuário encontrado ou None se não existir
        """
        pass

    @abstractmethod
    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        """
        Busca um usuário pelo email.

        Args:
            email: Email do usuário

        Returns:
            O usuário encontrado ou None se não existir
        """
        pass

    @abstractmethod
    def buscar_por_empresa(self, empresa_id: int) -> List[Usuario]:
        """
        Busca todos os usuários de uma empresa.

        Args:
            empresa_id: ID da empresa

        Returns:
            Lista de usuários da empresa
        """
        pass
