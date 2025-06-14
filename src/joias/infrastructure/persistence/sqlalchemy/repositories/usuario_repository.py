"""
Repositório de usuários.

Este módulo implementa o repositório de usuários usando SQLAlchemy,
seguindo o padrão Repository do DDD.
"""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from .....domain.identity.entities.usuario import Usuario
from .....domain.shared.value_objects.email import Email
from ....persistence.sqlalchemy.models import Usuario as UsuarioModel


class UsuarioRepository:
    """
    Repositório de usuários.

    Esta classe implementa as operações de persistência
    para a entidade Usuario usando SQLAlchemy.
    """

    def __init__(self, session: Session):
        """
        Inicializa o repositório.

        Args:
            session: Sessão do SQLAlchemy
        """
        self.session = session

    def proximo_id(self) -> UUID:
        """
        Gera o próximo ID para um novo usuário.

        Returns:
            UUID: Novo identificador único
        """
        return UUID.uuid4()

    def salvar(self, usuario: Usuario) -> Usuario:
        """
        Persiste um usuário no banco de dados.

        Args:
            usuario: Usuário a ser salvo

        Returns:
            Usuario: Usuário salvo

        Raises:
            ValueError: Se houver erro de validação
        """
        model = UsuarioModel(
            id=usuario.id,
            email=str(usuario.email),
            nome=usuario.nome,
            senha_hash=usuario.senha_hash,
            ativo=usuario.ativo,
            empresa_id=usuario.empresa_id if usuario.empresa_id else None
        )

        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)

        return self._to_entity(model)

    def buscar_por_id(self, id: UUID) -> Optional[Usuario]:
        """
        Busca um usuário pelo ID.

        Args:
            id: ID do usuário

        Returns:
            Optional[Usuario]: Usuário encontrado ou None
        """
        model = self.session.query(UsuarioModel).filter(
            UsuarioModel.id == id
        ).first()

        if model:
            return self._to_entity(model)
        return None

    def buscar_por_email(self, email: Email) -> Optional[Usuario]:
        """
        Busca um usuário pelo email.

        Args:
            email: Email do usuário

        Returns:
            Optional[Usuario]: Usuário encontrado ou None
        """
        model = self.session.query(UsuarioModel).filter(
            UsuarioModel.email == str(email)
        ).first()

        if model:
            return self._to_entity(model)
        return None

    def listar(self, apenas_ativos: bool = True) -> List[Usuario]:
        """
        Lista todos os usuários.

        Args:
            apenas_ativos: Se True, retorna apenas usuários ativos

        Returns:
            List[Usuario]: Lista de usuários
        """
        query = self.session.query(UsuarioModel)
        if apenas_ativos:
            query = query.filter(UsuarioModel.ativo == True)

        return [self._to_entity(model) for model in query.all()]

    def excluir(self, id: UUID) -> bool:
        """
        Remove um usuário do banco de dados.

        Args:
            id: ID do usuário

        Returns:
            bool: True se removido com sucesso
        """
        model = self.session.query(UsuarioModel).filter(
            UsuarioModel.id == id
        ).first()

        if model:
            self.session.delete(model)
            self.session.commit()
            return True
        return False

    def _to_entity(self, model: UsuarioModel) -> Usuario:
        """
        Converte um modelo do SQLAlchemy para uma entidade.

        Args:
            model: Modelo do SQLAlchemy

        Returns:
            Usuario: Entidade de usuário
        """
        return Usuario(
            id=model.id,
            email=Email(model.email),
            nome=model.nome,
            senha_hash=model.senha_hash,
            ativo=model.ativo,
            empresa_id=model.empresa_id if model.empresa_id else None,
            created_at=model.created_at,
            updated_at=model.updated_at,
            deleted_at=model.deleted_at
        ) 