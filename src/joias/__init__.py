"""
Sistema de Joias.

Este é o pacote principal do sistema de joias, que contém todos os módulos
e funcionalidades necessários para gerenciar um negócio de joias.
"""

from .domain.shared.entities.aggregate_root import AggregateRoot
from .domain.shared.events.domain_event import DomainEvent
from .domain.shared.repositories.repository import Repository
from .domain.shared.value_objects.value_object import ValueObject
from .infrastructure.persistence.sqlalchemy.models import (
    Usuario,
    Empresa,
    Endereco,
    Perfil,
    Permissao,
)

__all__ = [
    # Shared
    "AggregateRoot",
    "DomainEvent",
    "Repository",
    "ValueObject",
    # Models
    "Usuario",
    "Empresa",
    "Endereco",
    "Perfil",
    "Permissao",
]

"""
Exporta os módulos do pacote joias.
"""
from src.joias.infrastructure import (
    Settings,
    get_settings,
    Base,
    PerfilRepository,
    TokenRepository,
    UsuarioRepository,
)

__all__ = [
    "Settings",
    "get_settings",
    "Base",
    "PerfilRepository",
    "TokenRepository",
    "UsuarioRepository",
]
