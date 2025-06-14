"""
Interface do repositório de usuários.

Este módulo define a interface para persistência de usuários,
seguindo o padrão Repository do DDD.
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from ...shared.value_objects.email import Email
from ..entities.usuario import Usuario


class IUsuarioRepository(ABC):
    """
    Interface do repositório de usuários.

    Esta interface define os métodos que devem ser implementados
    por qualquer repositório concreto de usuários.
    """

    @abstractmethod
    def criar(self, usuario: Usuario) -> Usuario:
        """
        Persiste um novo usuário.

        Args:
            usuario: O usuário a ser persistido

        Returns:
            O usuário persistido

        Raises:
            ValueError: Se o email já existir
        """
        pass

    @abstractmethod
    def buscar_por_id(self, id: str) -> Optional[Usuario]:
        """
        Busca um usuário pelo seu ID.

        Args:
            id: O ID do usuário

        Returns:
            O usuário encontrado ou None
        """
        pass

    @abstractmethod
    def buscar_por_email(self, email: Email) -> Optional[Usuario]:
        """
        Busca um usuário pelo seu email.

        Args:
            email: O email do usuário

        Returns:
            O usuário encontrado ou None
        """
        pass

    @abstractmethod
    def listar(
        self,
        pagina: int = 1,
        tamanho: int = 10,
        email: Optional[str] = None,
        nome: Optional[str] = None,
    ) -> List[Usuario]:
        """
        Lista usuários com paginação e filtros opcionais.

        Args:
            pagina: Número da página (1-based)
            tamanho: Tamanho da página
            email: Filtro por email
            nome: Filtro por nome

        Returns:
            Lista de usuários
        """
        pass

    @abstractmethod
    def atualizar(self, usuario: Usuario) -> Usuario:
        """
        Atualiza um usuário existente.

        Args:
            usuario: O usuário com as alterações

        Returns:
            O usuário atualizado

        Raises:
            ValueError: Se o usuário não existir
        """
        pass

    @abstractmethod
    def excluir(self, id: str) -> None:
        """
        Remove um usuário do repositório.

        Args:
            id: O ID do usuário

        Raises:
            ValueError: Se o usuário não existir
        """
        pass
