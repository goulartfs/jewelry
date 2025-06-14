"""
Classe base para eventos de domínio.

Esta classe fornece a estrutura básica para eventos de domínio,
incluindo metadados como data de ocorrência.
"""
from abc import ABC
from datetime import datetime
from typing import Optional


class DomainEvent(ABC):
    """Classe base para eventos de domínio."""
    
    def __init__(self):
        """
        Inicializa um novo evento de domínio.
        
        O evento é automaticamente marcado com a data e hora atual
        de ocorrência.
        """
        self._occurred_on: datetime = datetime.now()
        
    @property
    def occurred_on(self) -> datetime:
        """
        Retorna a data e hora em que o evento ocorreu.
        
        Returns:
            A data e hora de ocorrência do evento.
        """
        return self._occurred_on
