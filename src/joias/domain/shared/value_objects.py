"""
Value objects do domínio.
"""
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Email:
    """
    Value object para email.
    """

    value: str

    def __post_init__(self):
        """
        Valida o email.
        """
        if not self.value:
            raise ValueError("Email não pode ser vazio")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.value):
            raise ValueError("Email inválido")

        if len(self.value) > 255:
            raise ValueError("Email não pode ter mais de 255 caracteres")

    def __str__(self):
        """
        Retorna o email como string.
        """
        return self.value 