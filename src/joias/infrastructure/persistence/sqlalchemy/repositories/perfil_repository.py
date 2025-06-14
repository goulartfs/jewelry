"""
Repositório SQLAlchemy para perfis.

Este módulo implementa o repositório de perfis usando
SQLAlchemy como ORM.
"""
from typing import Optional
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.joias.domain.entities.autorizacao import Perfil
from src.joias.infrastructure.persistence.sqlalchemy.models import Perfil as PerfilModel


class PerfilRepository:
    """Repositório SQLAlchemy para perfis."""

    def __init__(self, session: Session):
        """
        Inicializa o repositório.
        
        Args:
            session: Sessão do SQLAlchemy
        """
        self._session = session

    def criar(self, perfil: Perfil) -> Perfil:
        """
        Cria um novo perfil.
        
        Args:
            perfil: Perfil a ser criado
            
        Returns:
            O perfil criado
            
        Raises:
            IntegrityError: Se o nome já estiver em uso
        """
        try:
            perfil_model = PerfilModel(
                id=perfil.id,
                nome=perfil.nome,
                descricao=perfil.descricao,
                created_at=perfil.created_at,
                updated_at=perfil.updated_at,
                deleted_at=perfil.deleted_at,
            )
            self._session.add(perfil_model)
            self._session.commit()
            return perfil
        except IntegrityError:
            self._session.rollback()
            raise

    def buscar_por_id(self, id: UUID) -> Optional[Perfil]:
        """
        Busca um perfil pelo ID.
        
        Args:
            id: ID do perfil
            
        Returns:
            O perfil encontrado ou None se não existir
        """
        perfil_model = self._session.query(PerfilModel).filter_by(id=id).first()
        if not perfil_model:
            return None
        return Perfil(
            id=perfil_model.id,
            nome=perfil_model.nome,
            descricao=perfil_model.descricao,
            created_at=perfil_model.created_at,
            updated_at=perfil_model.updated_at,
            deleted_at=perfil_model.deleted_at,
        )

    def buscar_por_nome(self, nome: str) -> Optional[Perfil]:
        """
        Busca um perfil pelo nome.
        
        Args:
            nome: Nome do perfil
            
        Returns:
            O perfil encontrado ou None se não existir
        """
        perfil_model = self._session.query(PerfilModel).filter_by(nome=nome).first()
        if not perfil_model:
            return None
        return Perfil(
            id=perfil_model.id,
            nome=perfil_model.nome,
            descricao=perfil_model.descricao,
            created_at=perfil_model.created_at,
            updated_at=perfil_model.updated_at,
            deleted_at=perfil_model.deleted_at,
        )

    def atualizar(self, perfil: Perfil) -> Perfil:
        """
        Atualiza um perfil existente.
        
        Args:
            perfil: Perfil a ser atualizado
            
        Returns:
            O perfil atualizado
            
        Raises:
            IntegrityError: Se o nome já estiver em uso
        """
        try:
            perfil_model = self._session.query(PerfilModel).filter_by(id=perfil.id).first()
            if not perfil_model:
                raise ValueError(f"Perfil com ID {perfil.id} não encontrado")
            
            perfil_model.nome = perfil.nome
            perfil_model.descricao = perfil.descricao
            perfil_model.updated_at = perfil.updated_at
            perfil_model.deleted_at = perfil.deleted_at
            
            self._session.commit()
            return perfil
        except IntegrityError:
            self._session.rollback()
            raise

    def excluir(self, id: UUID) -> None:
        """
        Exclui um perfil.
        
        Args:
            id: ID do perfil a ser excluído
        """
        perfil_model = self._session.query(PerfilModel).filter_by(id=id).first()
        if perfil_model:
            self._session.delete(perfil_model)
            self._session.commit() 