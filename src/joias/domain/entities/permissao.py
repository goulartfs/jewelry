"""
Entidade de permissão do sistema.

Esta classe representa uma permissão no sistema, que pode ser associada
a perfis para controle de acesso.
"""
from typing import Optional

from ..shared.entities.aggregate_root import AggregateRoot


class Permissao(AggregateRoot):
    """
    Entidade que representa uma permissão no sistema.

    Esta classe implementa as regras de negócio relacionadas
    às permissões, incluindo validações e comportamentos.

    Attributes:
        nome: Nome descritivo da permissão
        chave: Chave única usada no código para verificação
        descricao: Descrição detalhada da permissão
    """

    def __init__(
        self,
        nome: str,
        chave: str,
        descricao: Optional[str] = None,
    ) -> None:
        """
        Inicializa uma nova permissão.

        Args:
            nome: Nome descritivo da permissão
            chave: Chave única usada no código
            descricao: Descrição detalhada (opcional)

        Raises:
            ValueError: Se o nome ou chave estiverem vazios
        """
        super().__init__()

        if not nome or not nome.strip():
            raise ValueError("Nome da permissão não pode estar vazio")
        
        if not chave or not chave.strip():
            raise ValueError("Chave da permissão não pode estar vazia")

        self._nome = nome.strip()
        self._chave = chave.strip().upper()
        self._descricao = descricao.strip() if descricao else None

    @property
    def nome(self) -> str:
        """Retorna o nome da permissão."""
        return self._nome

    @property
    def chave(self) -> str:
        """Retorna a chave da permissão."""
        return self._chave

    @property
    def descricao(self) -> Optional[str]:
        """Retorna a descrição da permissão."""
        return self._descricao 