"""
Serviço de usuários.

Este módulo implementa o serviço de usuários da aplicação,
incluindo operações de CRUD e regras de negócio específicas.
"""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from ...domain.identity.entities.usuario import Usuario
from ...domain.shared.value_objects.email import Email
from ...infrastructure.persistence.sqlalchemy.repositories.usuario_repository import UsuarioRepository
from ..identity.auth_service import AuthService


class UserService:
    """
    Serviço de usuários.

    Esta classe implementa a lógica de negócio relacionada
    a usuários, incluindo:
    - Criação de usuários
    - Atualização de dados
    - Busca e listagem
    - Remoção de usuários
    """

    def __init__(self, db: Session):
        """
        Inicializa o serviço de usuários.

        Args:
            db: Sessão do banco de dados
        """
        self.db = db
        self.usuario_repository = UsuarioRepository(db)
        self.auth_service = AuthService(db)

    def create_user(
        self,
        email: Email,
        nome: str,
        senha: str,
        empresa_id: Optional[UUID] = None
    ) -> Usuario:
        """
        Cria um novo usuário.

        Args:
            email: Email do usuário
            nome: Nome do usuário
            senha: Senha em texto plano
            empresa_id: ID da empresa (opcional)

        Returns:
            Usuario: Usuário criado

        Raises:
            ValueError: Se houver erro de validação
        """
        # Verifica se já existe usuário com o mesmo email
        existing = self.usuario_repository.buscar_por_email(email)
        if existing:
            raise ValueError("Email já cadastrado")

        # Cria o usuário
        usuario = Usuario(
            id=self.usuario_repository.proximo_id(),
            email=email,
            nome=nome,
            senha_hash=self.auth_service.get_password_hash(senha),
            empresa_id=empresa_id
        )

        return self.usuario_repository.salvar(usuario)

    def get_user(self, user_id: str) -> Optional[Usuario]:
        """
        Busca um usuário pelo ID.

        Args:
            user_id: ID do usuário

        Returns:
            Optional[Usuario]: Usuário encontrado ou None
        """
        return self.usuario_repository.buscar_por_id(UUID(user_id))

    def get_user_by_email(self, email: Email) -> Optional[Usuario]:
        """
        Busca um usuário pelo email.

        Args:
            email: Email do usuário

        Returns:
            Optional[Usuario]: Usuário encontrado ou None
        """
        return self.usuario_repository.buscar_por_email(email)

    def list_users(
        self,
        empresa_id: Optional[UUID] = None,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None
    ) -> List[Usuario]:
        """
        Lista usuários com filtros.

        Args:
            empresa_id: ID da empresa para filtrar
            skip: Número de registros para pular
            limit: Número máximo de registros
            search: Termo de busca

        Returns:
            List[Usuario]: Lista de usuários
        """
        return self.usuario_repository.listar(apenas_ativos=True)

    def update_user(
        self,
        user_id: str,
        email: Optional[Email] = None,
        nome: Optional[str] = None,
        senha: Optional[str] = None
    ) -> Usuario:
        """
        Atualiza os dados de um usuário.

        Args:
            user_id: ID do usuário
            email: Novo email
            nome: Novo nome
            senha: Nova senha

        Returns:
            Usuario: Usuário atualizado

        Raises:
            ValueError: Se houver erro de validação
        """
        usuario = self.usuario_repository.buscar_por_id(UUID(user_id))
        if not usuario:
            raise ValueError("Usuário não encontrado")

        if email:
            # Verifica se o novo email já está em uso
            existing = self.usuario_repository.buscar_por_email(email)
            if existing and existing.id != usuario.id:
                raise ValueError("Email já cadastrado")
            usuario.atualizar_email(email)

        if nome:
            usuario.atualizar_nome(nome)

        if senha:
            senha_hash = self.auth_service.get_password_hash(senha)
            usuario.atualizar_senha(senha_hash)

        return self.usuario_repository.salvar(usuario)

    def delete_user(self, user_id: str) -> None:
        """
        Remove um usuário.

        Args:
            user_id: ID do usuário

        Raises:
            ValueError: Se o usuário não for encontrado
        """
        usuario = self.usuario_repository.buscar_por_id(UUID(user_id))
        if not usuario:
            raise ValueError("Usuário não encontrado")

        usuario.desativar()
        self.usuario_repository.salvar(usuario) 