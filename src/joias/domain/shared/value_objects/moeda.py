"""
Objeto de valor que representa uma moeda.

Este módulo define a estrutura e comportamento de uma moeda no sistema,
incluindo seu código ISO, nome e símbolo.
"""
from dataclasses import dataclass
from typing import ClassVar, Dict


@dataclass(frozen=True)
class Moeda:
    """
    Representa uma moeda no sistema.

    Esta é uma classe imutável (frozen) que representa uma moeda,
    contendo seu código ISO 4217, nome e símbolo.

    Attributes:
        codigo: Código ISO 4217 da moeda (ex: 'BRL', 'USD')
        nome: Nome completo da moeda (ex: 'Real Brasileiro')
        simbolo: Símbolo da moeda (ex: 'R$')
    """
    codigo: str
    nome: str
    simbolo: str

    # Moedas pré-definidas para uso comum
    BRL: ClassVar['Moeda']
    USD: ClassVar['Moeda']
    EUR: ClassVar['Moeda']

    def __post_init__(self):
        """Validação após inicialização."""
        if len(self.codigo) != 3:
            raise ValueError(
                "O código da moeda deve ser uma string de 3 letras "
                "(ex: 'BRL', 'USD')."
            )
        if not self.nome:
            raise ValueError("O nome da moeda não pode ser vazio.")
        if not self.simbolo:
            raise ValueError("O símbolo da moeda não pode ser vazio.")

        # Força o código para maiúsculas
        object.__setattr__(self, 'codigo', self.codigo.upper())

    def __str__(self) -> str:
        """Retorna uma representação legível da moeda."""
        return f"{self.nome} ({self.codigo}) - {self.simbolo}"

    def __repr__(self) -> str:
        """Retorna uma representação oficial da moeda."""
        return f"Moeda(codigo='{self.codigo}', nome='{self.nome}', simbolo='{self.simbolo}')"


# Definição das moedas mais comuns
Moeda.BRL = Moeda("BRL", "Real Brasileiro", "R$")
Moeda.USD = Moeda("USD", "Dólar Americano", "$")
Moeda.EUR = Moeda("EUR", "Euro", "€") 