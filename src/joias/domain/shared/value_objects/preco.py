"""
Objeto de valor que representa um preço.

Este módulo define a estrutura e comportamento de um preço no sistema,
incluindo seu valor em centavos e moeda associada.
"""
from dataclasses import dataclass
from decimal import Decimal
from typing import Union

from .moeda import Moeda


@dataclass(frozen=True)
class Preco:
    """
    Representa um preço no sistema.

    Esta é uma classe imutável (frozen) que representa um preço,
    contendo seu valor em centavos e a moeda associada.

    Attributes:
        valor_em_centavos: Valor monetário em centavos (ex: R$10,90 = 1090)
        moeda: Moeda do preço
    """

    valor_em_centavos: int
    moeda: Moeda

    def __post_init__(self):
        """Validação após inicialização."""
        if not isinstance(self.valor_em_centavos, int):
            raise TypeError("O valor deve ser um número inteiro em centavos.")
        if not isinstance(self.moeda, Moeda):
            raise TypeError("A moeda deve ser uma instância da classe Moeda.")

    @property
    def valor(self) -> Decimal:
        """Retorna o valor como Decimal para cálculos precisos."""
        return Decimal(self.valor_em_centavos) / 100

    def __add__(self, outro: "Preco") -> "Preco":
        """Soma dois preços da mesma moeda."""
        if not isinstance(outro, Preco):
            return NotImplemented
        if self.moeda != outro.moeda:
            raise ValueError("Não é possível somar preços de moedas diferentes.")
        return Preco(
            valor_em_centavos=self.valor_em_centavos + outro.valor_em_centavos,
            moeda=self.moeda,
        )

    def __sub__(self, outro: "Preco") -> "Preco":
        """Subtrai dois preços da mesma moeda."""
        if not isinstance(outro, Preco):
            return NotImplemented
        if self.moeda != outro.moeda:
            raise ValueError("Não é possível subtrair preços de moedas diferentes.")
        return Preco(
            valor_em_centavos=self.valor_em_centavos - outro.valor_em_centavos,
            moeda=self.moeda,
        )

    def __mul__(self, multiplicador: Union[int, float, Decimal]) -> "Preco":
        """Multiplica o preço por um número."""
        if not isinstance(multiplicador, (int, float, Decimal)):
            return NotImplemented
        novo_valor = int(round(self.valor_em_centavos * Decimal(str(multiplicador))))
        return Preco(valor_em_centavos=novo_valor, moeda=self.moeda)

    def __truediv__(self, divisor: Union[int, float, Decimal]) -> "Preco":
        """Divide o preço por um número."""
        if not isinstance(divisor, (int, float, Decimal)):
            return NotImplemented
        if divisor == 0:
            raise ValueError("Não é possível dividir por zero.")
        novo_valor = int(round(self.valor_em_centavos / Decimal(str(divisor))))
        return Preco(valor_em_centavos=novo_valor, moeda=self.moeda)

    def __str__(self) -> str:
        """Retorna uma representação legível do preço."""
        return f"{self.moeda.simbolo}{self.valor:.2f}"

    def __repr__(self) -> str:
        """Retorna uma representação oficial do preço."""
        return (
            f"Preco(valor_em_centavos={self.valor_em_centavos}, moeda={self.moeda!r})"
        )

    def __eq__(self, outro: object) -> bool:
        """Compara dois preços."""
        if not isinstance(outro, Preco):
            return NotImplemented
        return (
            self.valor_em_centavos == outro.valor_em_centavos
            and self.moeda == outro.moeda
        )

    def __lt__(self, outro: "Preco") -> bool:
        """Compara se este preço é menor que outro."""
        if not isinstance(outro, Preco):
            return NotImplemented
        if self.moeda != outro.moeda:
            raise ValueError("Não é possível comparar preços de moedas diferentes.")
        return self.valor_em_centavos < outro.valor_em_centavos

    def aplicar_desconto(self, percentual: Union[int, float, Decimal]) -> "Preco":
        """
        Aplica um desconto percentual ao preço.

        Args:
            percentual: Valor do desconto (0-100)

        Returns:
            Preco: Novo preço com desconto aplicado

        Raises:
            ValueError: Se o percentual não estiver entre 0 e 100
        """
        if not 0 <= float(percentual) <= 100:
            raise ValueError("O percentual de desconto deve estar entre 0 e 100.")
        fator = (100 - Decimal(str(percentual))) / 100
        return self * fator
