"""
Repositório SQLAlchemy para tokens.

Este módulo implementa o repositório de tokens usando
SQLAlchemy como ORM.
"""
from typing import Optional
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.joias.domain.entities.autorizacao import Token
from src.joias.infrastructure.persistence.sqlalchemy.models import Token as TokenModel


class TokenRepository:
    """Repositório SQLAlchemy para tokens."""

    def __init__(self, session: Session):
        """
        Inicializa o repositório.
        
        Args:
            session: Sessão do SQLAlchemy
        """
        self._session = session

    def criar(self, token: Token) -> Token:
        """
        Cria um novo token.
        
        Args:
            token: Token a ser criado
            
        Returns:
            O token criado
            
        Raises:
            IntegrityError: Se houver erro de integridade
        """
        try:
            token_model = TokenModel(
                id=token.id,
                usuario_id=token.usuario_id,
                token=token.token,
                expiracao=token.expiracao,
                created_at=token.created_at,
                updated_at=token.updated_at,
                deleted_at=token.deleted_at,
            )
            self._session.add(token_model)
            self._session.commit()
            return token
        except IntegrityError:
            self._session.rollback()
            raise

    def buscar_por_id(self, id: UUID) -> Optional[Token]:
        """
        Busca um token pelo ID.
        
        Args:
            id: ID do token
            
        Returns:
            O token encontrado ou None se não existir
        """
        token_model = self._session.query(TokenModel).filter_by(id=id).first()
        if not token_model:
            return None
        return Token(
            id=token_model.id,
            usuario_id=token_model.usuario_id,
            token=token_model.token,
            expiracao=token_model.expiracao,
            created_at=token_model.created_at,
            updated_at=token_model.updated_at,
            deleted_at=token_model.deleted_at,
        )

    def buscar_por_token(self, token: str) -> Optional[Token]:
        """
        Busca um token pelo valor do token.
        
        Args:
            token: Valor do token
            
        Returns:
            O token encontrado ou None se não existir
        """
        token_model = self._session.query(TokenModel).filter_by(token=token).first()
        if not token_model:
            return None
        return Token(
            id=token_model.id,
            usuario_id=token_model.usuario_id,
            token=token_model.token,
            expiracao=token_model.expiracao,
            created_at=token_model.created_at,
            updated_at=token_model.updated_at,
            deleted_at=token_model.deleted_at,
        )

    def buscar_por_usuario_id(self, usuario_id: UUID) -> Optional[Token]:
        """
        Busca um token pelo ID do usuário.
        
        Args:
            usuario_id: ID do usuário
            
        Returns:
            O token encontrado ou None se não existir
        """
        token_model = self._session.query(TokenModel).filter_by(usuario_id=usuario_id).first()
        if not token_model:
            return None
        return Token(
            id=token_model.id,
            usuario_id=token_model.usuario_id,
            token=token_model.token,
            expiracao=token_model.expiracao,
            created_at=token_model.created_at,
            updated_at=token_model.updated_at,
            deleted_at=token_model.deleted_at,
        )

    def atualizar(self, token: Token) -> Token:
        """
        Atualiza um token existente.
        
        Args:
            token: Token a ser atualizado
            
        Returns:
            O token atualizado
            
        Raises:
            IntegrityError: Se houver erro de integridade
            ValueError: Se o token não for encontrado
        """
        try:
            token_model = self._session.query(TokenModel).filter_by(id=token.id).first()
            if not token_model:
                raise ValueError(f"Token com ID {token.id} não encontrado")
            
            token_model.usuario_id = token.usuario_id
            token_model.token = token.token
            token_model.expiracao = token.expiracao
            token_model.updated_at = token.updated_at
            token_model.deleted_at = token.deleted_at
            
            self._session.commit()
            return token
        except IntegrityError:
            self._session.rollback()
            raise

    def excluir(self, id: UUID) -> None:
        """
        Exclui um token.
        
        Args:
            id: ID do token a ser excluído
        """
        token_model = self._session.query(TokenModel).filter_by(id=id).first()
        if token_model:
            self._session.delete(token_model)
            self._session.commit() 