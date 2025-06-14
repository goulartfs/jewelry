"""
Classe base para agregados do domínio.

Este módulo define a classe base para agregados do domínio,
seguindo os princípios do DDD.
"""
from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from ..events.domain_event import DomainEvent


class AggregateRoot(ABC):
    """
    Classe base para agregados do domínio.
    
    Esta classe fornece funcionalidades comuns a todos os
    agregados, como identidade e eventos de domínio.
    """
    
    def __init__(self) -> None:
        """Inicializa um novo agregado."""
        self._id = uuid4()
        self._eventos: List[object] = []
        
    @property
    def id(self) -> UUID:
        """Retorna o ID do agregado."""
        return self._id
        
    @property
    def eventos(self) -> List[object]:
        """Retorna os eventos pendentes do agregado."""
        return self._eventos.copy()
        
    def adicionar_evento(self, evento: object) -> None:
        """
        Adiciona um evento ao agregado.
        
        Args:
            evento: O evento a ser adicionado
        """
        self._eventos.append(evento)
        
    def limpar_eventos(self) -> None:
        """Limpa a lista de eventos pendentes."""
        self._eventos.clear()

    def add_domain_event(self, event: DomainEvent) -> None:
        """
        Adiciona um novo evento de domínio à lista de eventos pendentes.
        
        Args:
            event: O evento de domínio a ser adicionado.
        """
        self._eventos.append(event)

    def clear_domain_events(self) -> None:
        """Remove todos os eventos de domínio pendentes."""
        self._eventos.clear()

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