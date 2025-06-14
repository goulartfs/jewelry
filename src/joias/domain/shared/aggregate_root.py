"""
Classe base para agregados.
"""
from uuid import UUID


class AggregateRoot:
    """
    Classe base para agregados.
    """

    def __init__(self, id: UUID):
        """
        Inicializa o agregado.

        Args:
            id: ID do agregado
        """
        self._id = id

    @property
    def id(self) -> UUID:
        """
        Retorna o ID do agregado.
        """
        return self._id 