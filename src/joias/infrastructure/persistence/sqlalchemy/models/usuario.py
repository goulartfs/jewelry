"""
Modelo SQLAlchemy para usuários.

Este módulo define o modelo de usuário para persistência
usando SQLAlchemy como ORM.
"""
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Boolean

from ..base import Base


class UsuarioModel(Base):
    """
    Modelo SQLAlchemy para usuários.
    
    Esta classe mapeia a tabela de usuários no banco de dados,
    definindo suas colunas e relacionamentos.
    """
    
    __tablename__ = "usuarios"
    
    id = Column(String(36), primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    senha_hashed = Column(String(255), nullable=False)
    data_criacao = Column(DateTime, nullable=False, default=datetime.now)
    ativo = Column(Boolean, nullable=False, default=True)
    
    def __repr__(self) -> str:
        """Retorna uma representação legível do modelo."""
        return f"<Usuario {self.nome} ({self.email})>" 