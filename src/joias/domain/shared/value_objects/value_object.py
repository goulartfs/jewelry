"""
Classe base para objetos de valor.

Esta classe fornece a estrutura básica para implementação de
objetos de valor, incluindo comparação por valor.
"""
from abc import ABC
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ValueObject(ABC):
    """
    Classe base para objetos de valor.
    
    Esta classe usa o decorador @dataclass para gerar automaticamente
    os métodos __eq__ e __hash__, garantindo que a comparação seja
    feita por valor e não por referência.
    
    O parâmetro frozen=True garante que os objetos de valor sejam
    imutáveis após sua criação.
    """
    
    def __eq__(self, other: Any) -> bool:
        """
        Compara este objeto de valor com outro.
        
        A comparação é feita por valor, ou seja, dois objetos de valor
        são considerados iguais se todos os seus atributos são iguais.
        
        Args:
            other: O objeto a ser comparado.
        
        Returns:
            True se os objetos são iguais, False caso contrário.
        """
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__
