"""
Entidade de perfil do sistema.

Esta classe representa um perfil de usuário no sistema, que agrupa
um conjunto de permissões para controle de acesso.
"""
from datetime import datetime
from typing import List, Optional, Set

from ..shared.entities.aggregate_root import AggregateRoot
from .permissao import Permissao


class Perfil(AggregateRoot):
    """
    Entidade que representa um perfil de usuário no sistema.

    Esta classe implementa as regras de negócio relacionadas
    aos perfis, incluindo validações e comportamentos.

    Attributes:
        nome: Nome do perfil
        descricao: Descrição detalhada do perfil
        permissoes: Conjunto de permissões associadas
        data_criacao: Data de criação do registro
    """

    def __init__(
        self,
        nome: str,
        descricao: Optional[str] = None,
        data_criacao: Optional[datetime] = None,
    ) -> None:
        """
        Inicializa um novo perfil.

        Args:
            nome: Nome do perfil
            descricao: Descrição detalhada (opcional)
            data_criacao: Data de criação (opcional, default=now)

        Raises:
            ValueError: Se o nome estiver vazio
        """
        super().__init__()

        if not nome or not nome.strip():
            raise ValueError("Nome do perfil não pode estar vazio")

        self._nome = nome.strip()
        self._descricao = descricao.strip() if descricao else None
        self._data_criacao = data_criacao or datetime.now()
        self._permissoes: Set[Permissao] = set()

    @property
    def nome(self) -> str:
        """Retorna o nome do perfil."""
        return self._nome

    @property
    def descricao(self) -> Optional[str]:
        """Retorna a descrição do perfil."""
        return self._descricao

    @property
    def data_criacao(self) -> datetime:
        """Retorna a data de criação do perfil."""
        return self._data_criacao

    @property
    def permissoes(self) -> List[Permissao]:
        """Retorna a lista de permissões do perfil."""
        return list(self._permissoes)

    def adicionar_permissao(self, permissao: Permissao) -> None:
        """
        Adiciona uma permissão ao perfil.

        Args:
            permissao: Permissão a ser adicionada
        """
        self._permissoes.add(permissao)

    def remover_permissao(self, permissao: Permissao) -> None:
        """
        Remove uma permissão do perfil.

        Args:
            permissao: Permissão a ser removida
        """
        self._permissoes.discard(permissao)

    def tem_permissao(self, chave_permissao: str) -> bool:
        """
        Verifica se o perfil possui uma determinada permissão.

        Args:
            chave_permissao: Chave da permissão a ser verificada

        Returns:
            True se o perfil possui a permissão, False caso contrário
        """
        return any(p.chave == chave_permissao.upper() for p in self._permissoes) 