"""
Pacote compartilhado.

Este pacote contém classes e interfaces base compartilhadas
entre os diferentes contextos do domínio.
"""
from .entities.aggregate_root import AggregateRoot
from .events.domain_event import DomainEvent
from .value_objects.value_object import ValueObject
from .value_objects.email import Email

__all__ = [
    "AggregateRoot",
    "DomainEvent",
    "ValueObject",
    "Email"
]
