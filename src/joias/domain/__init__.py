"""
Pacote de domínio do sistema de joias.

Este pacote contém todos os módulos relacionados ao domínio do sistema,
organizados em bounded contexts seguindo os princípios do DDD.

Bounded Contexts:
- shared: Classes e interfaces base compartilhadas
- identity: Gerenciamento de identidade e acesso
- organization: Gestão da organização e seus membros
- catalog: Catálogo de produtos e fornecedores
- order: Pedidos e transações
"""

from .shared.entities.aggregate_root import AggregateRoot
from .shared.events.domain_event import DomainEvent
from .shared.repositories.repository import Repository
from .shared.value_objects.value_object import ValueObject

__all__ = ["AggregateRoot", "DomainEvent", "ValueObject", "Repository"]
