"""
Classe base para agregados do domínio.

Esta classe fornece a funcionalidade básica necessária para
implementar agregados do domínio, incluindo o gerenciamento
de eventos de domínio.
"""
from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from ..events.domain_event import DomainEvent


@dataclass
class AggregateRoot(ABC):
    """
    Classe base para agregados.

    Esta classe implementa funcionalidades comuns a todos os agregados
    como gerenciamento de eventos de domínio e controle de versão.

    Attributes:
        id: Identificador único do agregado
        version: Versão do agregado para controle de concorrência
        created_at: Data de criação
        updated_at: Data da última atualização
        deleted_at: Data de exclusão (soft delete)
        _events: Lista de eventos de domínio pendentes
    """

    id: UUID
    version: int = field(default=1)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = field(default=None)
    _events: List[DomainEvent] = field(default_factory=list, init=False)

    def __init__(self):
        """Inicializa um novo agregado."""
        self._domain_events: List[DomainEvent] = []

    @property
    def domain_events(self) -> List[DomainEvent]:
        """Retorna a lista de eventos de domínio pendentes."""
        return self._domain_events

    def add_domain_event(self, event: DomainEvent) -> None:
        """
        Adiciona um novo evento de domínio à lista de eventos pendentes.
        
        Args:
            event: O evento de domínio a ser adicionado.
        """
        self._domain_events.append(event)

    def clear_domain_events(self) -> None:
        """Remove todos os eventos de domínio pendentes."""
        self._domain_events.clear()

    def adicionar_evento(self, evento: DomainEvent) -> None:
        """
        Adiciona um evento de domínio à lista de eventos pendentes.

        Args:
            evento: O evento a ser adicionado
        """
        self._events.append(evento)

    def limpar_eventos(self) -> List[DomainEvent]:
        """
        Remove e retorna todos os eventos pendentes.

        Returns:
            List[DomainEvent]: Lista de eventos pendentes
        """
        eventos = self._events.copy()
        self._events.clear()
        return eventos

    def incrementar_versao(self) -> None:
        """Incrementa a versão do agregado."""
        self.version += 1
        self.updated_at = datetime.utcnow()

    def marcar_como_excluido(self) -> None:
        """Marca o agregado como excluído (soft delete)."""
        self.deleted_at = datetime.utcnow()

    @property
    def esta_ativo(self) -> bool:
        """
        Verifica se o agregado está ativo.

        Returns:
            bool: True se o agregado não foi excluído
        """
        return self.deleted_at is None

    def __eq__(self, other: object) -> bool:
        """
        Compara duas entidades pela sua identidade.

        Args:
            other: Objeto a ser comparado

        Returns:
            bool: True se as entidades têm o mesmo ID, False caso contrário
        """
        if not isinstance(other, AggregateRoot):
            return NotImplemented
        return self.id == other.id 