"""
Entidade de usuário do sistema.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from ..shared.aggregate_root import AggregateRoot
from ..shared.value_objects import Email


class Usuario(AggregateRoot):
    """
    Entidade que representa um usuário do sistema.
    """

    def __init__(
        self,
        nome: str,
        email: Email,
        senha_hash: str,
        ativo: bool = True,
        id: Optional[UUID] = None,
        data_criacao: Optional[datetime] = None,
    ):
        """
        Inicializa um novo usuário.

        Args:
            nome: Nome do usuário
            email: Email do usuário
            senha_hash: Hash da senha do usuário
            ativo: Se o usuário está ativo
            id: ID do usuário (opcional, gerado automaticamente se não fornecido)
            data_criacao: Data de criação do usuário (opcional, gerada automaticamente se não fornecida)
        """
        super().__init__(id or uuid4())
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash
        self.ativo = ativo
        self.data_criacao = data_criacao or datetime.utcnow()

    @property
    def nome(self) -> str:
        """Nome do usuário."""
        return self._nome

    @nome.setter
    def nome(self, value: str) -> None:
        """
        Define o nome do usuário.

        Args:
            value: Nome do usuário

        Raises:
            ValueError: Se o nome for vazio ou muito longo
        """
        if not value:
            raise ValueError("Nome não pode ser vazio")
        if len(value) > 100:
            raise ValueError("Nome não pode ter mais de 100 caracteres")
        self._nome = value

    @property
    def email(self) -> Email:
        """Email do usuário."""
        return self._email

    @email.setter
    def email(self, value: Email) -> None:
        """
        Define o email do usuário.

        Args:
            value: Email do usuário
        """
        self._email = value

    @property
    def senha_hash(self) -> str:
        """Hash da senha do usuário."""
        return self._senha_hash

    @senha_hash.setter
    def senha_hash(self, value: str) -> None:
        """
        Define o hash da senha do usuário.

        Args:
            value: Hash da senha

        Raises:
            ValueError: Se o hash da senha for vazio
        """
        if not value:
            raise ValueError("Hash da senha não pode ser vazio")
        self._senha_hash = value

    @property
    def ativo(self) -> bool:
        """Se o usuário está ativo."""
        return self._ativo

    @ativo.setter
    def ativo(self, value: bool) -> None:
        """
        Define se o usuário está ativo.

        Args:
            value: Se o usuário está ativo
        """
        self._ativo = value

    @property
    def data_criacao(self) -> datetime:
        """Data de criação do usuário."""
        return self._data_criacao

    @data_criacao.setter
    def data_criacao(self, value: datetime) -> None:
        """
        Define a data de criação do usuário.

        Args:
            value: Data de criação
        """
        self._data_criacao = value
