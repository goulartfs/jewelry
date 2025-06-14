"""
Repositório SQLAlchemy para usuários.

Este módulo implementa o repositório de usuários usando
SQLAlchemy como ORM.
"""
from typing import List, Optional
from uuid import UUID

from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.joias.domain.entities.autorizacao import Usuario, Perfil
from src.joias.infrastructure.persistence.sqlalchemy.models import (
    Usuario as UsuarioModel,
    Perfil as PerfilModel,
)


class UsuarioRepository:
    """Repositório SQLAlchemy para usuários."""

    def __init__(self, session: Session):
        """
        Inicializa o repositório.
        
        Args:
            session: Sessão do SQLAlchemy
        """
        self._session = session

    def criar(self, usuario: Usuario) -> Usuario:
        """
        Cria um novo usuário.
        
        Args:
            usuario: Usuário a ser criado
            
        Returns:
            O usuário criado
            
        Raises:
            IntegrityError: Se o email já estiver em uso
        """
        try:
            usuario_model = UsuarioModel(
                id=usuario.id,
                nome=usuario.nome,
                email=usuario.email,
                senha_hash=usuario.senha_hash,
                created_at=usuario.created_at,
                updated_at=usuario.updated_at,
                deleted_at=usuario.deleted_at,
            )
            self._session.add(usuario_model)
            self._session.commit()
            return usuario
        except IntegrityError:
            self._session.rollback()
            raise

    def buscar_por_id(self, id: UUID) -> Optional[Usuario]:
        """
        Busca um usuário pelo ID.
        
        Args:
            id: ID do usuário
            
        Returns:
            O usuário encontrado ou None se não existir
        """
        usuario_model = self._session.query(UsuarioModel).filter_by(id=id).first()
        if not usuario_model:
            return None
        return Usuario(
            id=usuario_model.id,
            nome=usuario_model.nome,
            email=usuario_model.email,
            senha_hash=usuario_model.senha_hash,
            created_at=usuario_model.created_at,
            updated_at=usuario_model.updated_at,
            deleted_at=usuario_model.deleted_at,
        )

    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        """
        Busca um usuário pelo email.
        
        Args:
            email: Email do usuário
            
        Returns:
            O usuário encontrado ou None se não existir
        """
        usuario_model = self._session.query(UsuarioModel).filter_by(email=email).first()
        if not usuario_model:
            return None
        return Usuario(
            id=usuario_model.id,
            nome=usuario_model.nome,
            email=usuario_model.email,
            senha_hash=usuario_model.senha_hash,
            created_at=usuario_model.created_at,
            updated_at=usuario_model.updated_at,
            deleted_at=usuario_model.deleted_at,
        )

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
        query = self._session.query(UsuarioModel)

        # Aplica filtros
        if email or nome:
            query = query.filter(
                or_(
                    UsuarioModel.email.ilike(f"%{email}%") if email else False,
                    UsuarioModel.nome.ilike(f"%{nome}%") if nome else False,
                )
            )

        # Aplica paginação
        offset = (pagina - 1) * tamanho
        query = query.offset(offset).limit(tamanho)

        # Converte para entidades
        return [self._to_entity(model) for model in query.all()]

    def atualizar(self, usuario: Usuario) -> Usuario:
        """
        Atualiza um usuário existente.
        
        Args:
            usuario: Usuário a ser atualizado
            
        Returns:
            O usuário atualizado
            
        Raises:
            IntegrityError: Se o email já estiver em uso
            ValueError: Se o usuário não for encontrado
        """
        try:
            usuario_model = self._session.query(UsuarioModel).filter_by(id=usuario.id).first()
            if not usuario_model:
                raise ValueError(f"Usuário com ID {usuario.id} não encontrado")
            
            usuario_model.nome = usuario.nome
            usuario_model.email = usuario.email
            usuario_model.senha_hash = usuario.senha_hash
            usuario_model.updated_at = usuario.updated_at
            usuario_model.deleted_at = usuario.deleted_at
            
            self._session.commit()
            return usuario
        except IntegrityError:
            self._session.rollback()
            raise

    def excluir(self, id: UUID) -> None:
        """
        Exclui um usuário.
        
        Args:
            id: ID do usuário a ser excluído
        """
        usuario_model = self._session.query(UsuarioModel).filter_by(id=id).first()
        if usuario_model:
            self._session.delete(usuario_model)
            self._session.commit()

    def associar_perfil(self, usuario_id: UUID, perfil_id: UUID) -> None:
        """
        Associa um perfil a um usuário.
        
        Args:
            usuario_id: ID do usuário
            perfil_id: ID do perfil
            
        Raises:
            ValueError: Se o usuário ou perfil não forem encontrados
            IntegrityError: Se houver erro de integridade
        """
        try:
            usuario_model = self._session.query(UsuarioModel).filter_by(id=usuario_id).first()
            if not usuario_model:
                raise ValueError(f"Usuário com ID {usuario_id} não encontrado")

            perfil_model = self._session.query(PerfilModel).filter_by(id=perfil_id).first()
            if not perfil_model:
                raise ValueError(f"Perfil com ID {perfil_id} não encontrado")

            usuario_model.perfis.append(perfil_model)
            self._session.commit()
        except IntegrityError:
            self._session.rollback()
            raise

    def desassociar_perfil(self, usuario_id: UUID, perfil_id: UUID) -> None:
        """
        Desassocia um perfil de um usuário.
        
        Args:
            usuario_id: ID do usuário
            perfil_id: ID do perfil
            
        Raises:
            ValueError: Se o usuário ou perfil não forem encontrados
        """
        usuario_model = self._session.query(UsuarioModel).filter_by(id=usuario_id).first()
        if not usuario_model:
            raise ValueError(f"Usuário com ID {usuario_id} não encontrado")

        perfil_model = self._session.query(PerfilModel).filter_by(id=perfil_id).first()
        if not perfil_model:
            raise ValueError(f"Perfil com ID {perfil_id} não encontrado")

        usuario_model.perfis.remove(perfil_model)
        self._session.commit()

    def listar_perfis(self, usuario_id: UUID) -> List[Perfil]:
        """
        Lista os perfis de um usuário.
        
        Args:
            usuario_id: ID do usuário
            
        Returns:
            Lista de perfis do usuário
            
        Raises:
            ValueError: Se o usuário não for encontrado
        """
        usuario_model = self._session.query(UsuarioModel).filter_by(id=usuario_id).first()
        if not usuario_model:
            raise ValueError(f"Usuário com ID {usuario_id} não encontrado")

        return [
            Perfil(
                id=perfil.id,
                nome=perfil.nome,
                descricao=perfil.descricao,
                created_at=perfil.created_at,
                updated_at=perfil.updated_at,
                deleted_at=perfil.deleted_at,
            )
            for perfil in usuario_model.perfis
        ]

    def _to_entity(self, model: UsuarioModel) -> Usuario:
        """
        Converte um modelo SQLAlchemy para uma entidade de domínio.

        Args:
            model: O modelo SQLAlchemy

        Returns:
            A entidade de domínio
        """
        return Usuario(
            id=model.id,
            nome=model.nome,
            email=model.email,
            senha_hash=model.senha_hash,
            created_at=model.created_at,
            updated_at=model.updated_at,
            deleted_at=model.deleted_at,
        )
