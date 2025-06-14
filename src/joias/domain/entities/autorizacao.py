"""
Entidades do domínio de autorização.

Este módulo contém as entidades relacionadas ao domínio
de autorização, como usuários, perfis e permissões.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from ..shared.entities.aggregate_root import AggregateRoot


class Usuario(AggregateRoot):
    """Entidade de usuário."""

    def __init__(
        self,
        id: UUID,
        email: str,
        nome: str,
        senha_hash: str,
        ativo: bool,
        created_at: datetime,
        updated_at: datetime,
        deleted_at: Optional[datetime] = None,
    ):
        """
        Inicializa um novo usuário.

        Args:
            id: ID do usuário
            email: E-mail do usuário
            nome: Nome do usuário
            senha_hash: Hash da senha do usuário
            ativo: Status de ativo do usuário
            created_at: Data de criação
            updated_at: Data de atualização
            deleted_at: Data de exclusão
        """
        self.id = id
        self.email = email
        self.nome = nome
        self.senha_hash = senha_hash
        self.ativo = ativo
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    @classmethod
    def criar(cls, email: str, nome: str, senha_hash: str) -> "Usuario":
        """
        Cria um novo usuário.

        Args:
            email: E-mail do usuário
            nome: Nome do usuário
            senha_hash: Hash da senha do usuário

        Returns:
            O usuário criado
        """
        now = datetime.now()
        return cls(
            id=uuid4(),
            email=email,
            nome=nome,
            senha_hash=senha_hash,
            ativo=True,
            created_at=now,
            updated_at=now,
        )

    def atualizar(
        self,
        email: Optional[str] = None,
        nome: Optional[str] = None,
        senha_hash: Optional[str] = None,
        ativo: Optional[bool] = None,
    ) -> None:
        """
        Atualiza os dados do usuário.

        Args:
            email: Novo e-mail
            nome: Novo nome
            senha_hash: Novo hash da senha
            ativo: Novo status de ativo
        """
        if email is not None:
            self.email = email
        if nome is not None:
            self.nome = nome
        if senha_hash is not None:
            self.senha_hash = senha_hash
        if ativo is not None:
            self.ativo = ativo
        self.updated_at = datetime.now()

    def excluir(self) -> None:
        """Marca o usuário como excluído."""
        self.ativo = False
        self.deleted_at = datetime.now()
        self.updated_at = datetime.now()


class Perfil(AggregateRoot):
    """Entidade de perfil."""

    def __init__(
        self,
        id: UUID,
        nome: str,
        descricao: Optional[str],
        created_at: datetime,
        updated_at: datetime,
        deleted_at: Optional[datetime] = None,
    ):
        """
        Inicializa um novo perfil.

        Args:
            id: ID do perfil
            nome: Nome do perfil
            descricao: Descrição do perfil
            created_at: Data de criação
            updated_at: Data de atualização
            deleted_at: Data de exclusão
        """
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    @classmethod
    def criar(cls, nome: str, descricao: Optional[str] = None) -> "Perfil":
        """
        Cria um novo perfil.

        Args:
            nome: Nome do perfil
            descricao: Descrição do perfil

        Returns:
            O perfil criado
        """
        now = datetime.now()
        return cls(
            id=uuid4(),
            nome=nome,
            descricao=descricao,
            created_at=now,
            updated_at=now,
        )

    def atualizar(
        self,
        nome: Optional[str] = None,
        descricao: Optional[str] = None,
    ) -> None:
        """
        Atualiza os dados do perfil.

        Args:
            nome: Novo nome
            descricao: Nova descrição
        """
        if nome is not None:
            self.nome = nome
        if descricao is not None:
            self.descricao = descricao
        self.updated_at = datetime.now()

    def excluir(self) -> None:
        """Marca o perfil como excluído."""
        self.deleted_at = datetime.now()
        self.updated_at = datetime.now()


class Permissao(AggregateRoot):
    """Entidade de permissão."""

    def __init__(
        self,
        id: UUID,
        nome: str,
        descricao: Optional[str],
        created_at: datetime,
        updated_at: datetime,
        deleted_at: Optional[datetime] = None,
    ):
        """
        Inicializa uma nova permissão.

        Args:
            id: ID da permissão
            nome: Nome da permissão
            descricao: Descrição da permissão
            created_at: Data de criação
            updated_at: Data de atualização
            deleted_at: Data de exclusão
        """
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    @classmethod
    def criar(cls, nome: str, descricao: Optional[str] = None) -> "Permissao":
        """
        Cria uma nova permissão.

        Args:
            nome: Nome da permissão
            descricao: Descrição da permissão

        Returns:
            A permissão criada
        """
        now = datetime.now()
        return cls(
            id=uuid4(),
            nome=nome,
            descricao=descricao,
            created_at=now,
            updated_at=now,
        )

    def atualizar(
        self,
        nome: Optional[str] = None,
        descricao: Optional[str] = None,
    ) -> None:
        """
        Atualiza os dados da permissão.

        Args:
            nome: Novo nome
            descricao: Nova descrição
        """
        if nome is not None:
            self.nome = nome
        if descricao is not None:
            self.descricao = descricao
        self.updated_at = datetime.now()

    def excluir(self) -> None:
        """Marca a permissão como excluída."""
        self.deleted_at = datetime.now()
        self.updated_at = datetime.now()


class Token(AggregateRoot):
    """Entidade que representa um token de acesso."""

    def __init__(
        self,
        id: UUID,
        usuario_id: UUID,
        token: str,
        expiracao: datetime,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None,
    ):
        """
        Inicializa um token.
        
        Args:
            id: ID do token
            usuario_id: ID do usuário
            token: Token de acesso
            expiracao: Data de expiração
            created_at: Data de criação
            updated_at: Data de atualização
            deleted_at: Data de exclusão
        """
        self.id = id
        self.usuario_id = usuario_id
        self.token = token
        self.expiracao = expiracao
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.deleted_at = deleted_at

    @classmethod
    def criar(cls, usuario_id: UUID, token: str, expiracao: datetime) -> "Token":
        """
        Cria um novo token.

        Args:
            usuario_id: ID do usuário
            token: Token de acesso
            expiracao: Data de expiração

        Returns:
            O token criado
        """
        return cls(
            id=uuid4(),
            usuario_id=usuario_id,
            token=token,
            expiracao=expiracao,
        )

    def atualizar(
        self,
        token: Optional[str] = None,
        expiracao: Optional[datetime] = None,
    ) -> None:
        """
        Atualiza os dados do token.

        Args:
            token: Novo token
            expiracao: Nova data de expiração
        """
        if token is not None:
            self.token = token
        if expiracao is not None:
            self.expiracao = expiracao
        self.updated_at = datetime.now()

    def excluir(self) -> None:
        """Marca o token como excluído."""
        self.deleted_at = datetime.now()
        self.updated_at = datetime.now()
