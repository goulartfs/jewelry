"""
Repositório de usuários em memória.

Este módulo contém a implementação do repositório de usuários
em memória para testes.
"""
from typing import List, Optional

from ....domain.entities.usuario import Usuario
from ....domain.repositories.usuario import UsuarioRepository
from .base import MemoryRepository


class MemoryUsuarioRepository(MemoryRepository[Usuario], UsuarioRepository):
    """
    Implementação do repositório de usuários em memória.
    
    Esta implementação é útil para testes e desenvolvimento.
    """

    def buscar_por_username(self, username: str) -> Optional[Usuario]:
        """
        Busca um usuário pelo username.

        Args:
            username: Username do usuário

        Returns:
            O usuário encontrado ou None se não existir
        """
        return next(
            (u for u in self._items.values() if u.username == username),
            None
        )

    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        """
        Busca um usuário pelo email.

        Args:
            email: Email do usuário

        Returns:
            O usuário encontrado ou None se não existir
        """
        return next(
            (u for u in self._items.values() if u.email == email),
            None
        )

    def buscar_por_empresa(self, empresa_id: int) -> List[Usuario]:
        """
        Busca todos os usuários de uma empresa.

        Args:
            empresa_id: ID da empresa

        Returns:
            Lista de usuários da empresa
        """
        return [
            u for u in self._items.values()
            if u.empresa and u.empresa.id == empresa_id
        ] 