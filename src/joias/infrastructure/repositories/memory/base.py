"""
Repositório base em memória.

Este módulo contém a implementação base de um repositório
em memória para testes.
"""
from typing import Dict, Generic, List, Optional, TypeVar

from ....domain.entities.base import Entity
from ....domain.repositories.base import Repository

T = TypeVar("T", bound=Entity)


class MemoryRepository(Repository[T], Generic[T]):
    """
    Implementação base de um repositório em memória.

    Esta classe serve como base para implementações de repositórios
    em memória, úteis para testes.
    """

    def __init__(self):
        self._items: Dict[int, T] = {}
        self._next_id = 1

    def criar(self, item: T) -> T:
        """
        Cria um novo item no repositório.

        Args:
            item: Item a ser criado

        Returns:
            Item criado com ID atribuído
        """
        item.id = self._next_id
        self._items[item.id] = item
        self._next_id += 1
        return item

    def atualizar(self, item: T) -> T:
        """
        Atualiza um item existente no repositório.

        Args:
            item: Item a ser atualizado

        Returns:
            Item atualizado

        Raises:
            ValueError: Se o item não existir
        """
        if item.id not in self._items:
            raise ValueError("Item não encontrado")
        self._items[item.id] = item
        return item

    def deletar(self, item: T) -> None:
        """
        Remove um item do repositório.

        Args:
            item: Item a ser removido

        Raises:
            ValueError: Se o item não existir
        """
        if item.id not in self._items:
            raise ValueError("Item não encontrado")
        del self._items[item.id]

    def buscar_por_id(self, id: int) -> Optional[T]:
        """
        Busca um item pelo ID.

        Args:
            id: ID do item

        Returns:
            Item encontrado ou None se não existir
        """
        return self._items.get(id)

    def listar_todos(self) -> List[T]:
        """
        Lista todos os itens do repositório.

        Returns:
            Lista com todos os itens
        """
        return list(self._items.values())
