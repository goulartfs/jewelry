"""
Serviço de perfil.

Este módulo contém a lógica de negócio para operações
relacionadas a perfis de usuário.
"""
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from src.joias.domain.entities.autorizacao import Perfil
from src.joias.infrastructure.persistence.sqlalchemy.repositories.perfil_repository import (
    SQLPerfilRepository,
)


@dataclass
class CriarPerfilDTO:
    """DTO para criação de perfil."""
    nome: str
    descricao: Optional[str] = None


@dataclass
class AtualizarPerfilDTO:
    """DTO para atualização de perfil."""
    id: UUID
    nome: Optional[str] = None
    descricao: Optional[str] = None


@dataclass
class PerfilDTO:
    """DTO para retorno de dados do perfil."""
    id: UUID
    nome: str
    descricao: Optional[str]
    created_at: str
    updated_at: str


class PerfilService:
    """Serviço para gerenciamento de perfis."""

    def __init__(self, repository: SQLPerfilRepository):
        """
        Inicializa o serviço.
        
        Args:
            repository: Repositório de perfis
        """
        self._repository = repository

    def criar_perfil(self, dto: CriarPerfilDTO) -> PerfilDTO:
        """
        Cria um novo perfil.
        
        Args:
            dto: Dados do perfil a ser criado
            
        Returns:
            Dados do perfil criado
            
        Raises:
            ValueError: Se os dados forem inválidos ou houver conflito
        """
        # Validar nome único
        if self._repository.buscar_por_nome(dto.nome):
            raise ValueError(f"Já existe um perfil com o nome '{dto.nome}'")

        # Criar perfil
        perfil = Perfil(
            nome=dto.nome,
            descricao=dto.descricao
        )
        
        # Persistir
        perfil_criado = self._repository.criar(perfil)
        
        # Retornar DTO
        return PerfilDTO(
            id=perfil_criado.id,
            nome=perfil_criado.nome,
            descricao=perfil_criado.descricao,
            created_at=perfil_criado.created_at.isoformat(),
            updated_at=perfil_criado.updated_at.isoformat()
        )

    def associar_usuario(self, perfil_id: UUID, usuario_id: UUID) -> None:
        """
        Associa um usuário a um perfil.
        
        Args:
            perfil_id: ID do perfil
            usuario_id: ID do usuário
            
        Raises:
            ValueError: Se o perfil ou usuário não for encontrado
        """
        # Validar existência do perfil
        perfil = self._repository.buscar_por_id(perfil_id)
        if not perfil:
            raise ValueError(f"Perfil com ID '{perfil_id}' não encontrado")

        # Validar existência do usuário (feito no repositório)
        self._repository.associar_usuario(perfil_id, usuario_id) 