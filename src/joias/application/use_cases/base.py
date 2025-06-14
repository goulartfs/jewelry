"""
Classes base para casos de uso.

Este módulo contém as classes base que todos os casos de uso devem herdar.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

from ...domain.entities.base import Entity
from ...domain.repositories.base import Repository

Input = TypeVar("Input")
Output = TypeVar("Output")
E = TypeVar("E", bound=Entity)


@dataclass
class UseCase(Generic[Input, Output], ABC):
    """
    Classe base para todos os casos de uso.

    Um caso de uso representa uma ação específica que pode ser executada
    no sistema. Ele recebe dados de entrada, executa a lógica de negócio
    e retorna dados de saída.
    """

    @abstractmethod
    def execute(self, input_data: Input) -> Output:
        """
        Executa o caso de uso.

        Args:
            input_data: Dados de entrada para o caso de uso

        Returns:
            Dados de saída do caso de uso
        """
        pass


@dataclass
class EntityUseCase(UseCase[Input, Output], Generic[Input, Output, E]):
    """
    Classe base para casos de uso que manipulam entidades.

    Esta classe adiciona um repositório à classe base UseCase,
    facilitando a manipulação de entidades do domínio.
    """

    repository: Repository[E]
