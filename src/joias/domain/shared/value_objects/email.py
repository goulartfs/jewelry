"""
Objeto de valor para endereços de email.

Este módulo define um objeto de valor que representa
e valida endereços de email.
"""
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Email:
    """
    Objeto de valor para endereços de email.

    Esta classe encapsula a lógica de validação e representação
    de endereços de email, garantindo que apenas emails válidos
    sejam aceitos.

    Attributes:
        valor: O endereço de email
    """

    valor: str

    def __post_init__(self) -> None:
        """
        Valida o email após a inicialização.

        Raises:
            ValueError: Se o email for inválido
        """
        if not self.valor:
            raise ValueError("Email não pode estar vazio")

        if not self._is_valid_email(self.valor):
            raise ValueError(f"Email inválido: {self.valor}")

        # Força o email para minúsculas
        object.__setattr__(self, "valor", self.valor.lower())

    def __str__(self) -> str:
        """Retorna o email como string."""
        return self.valor

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """
        Verifica se um email é válido.

        Args:
            email: O email a ser validado

        Returns:
            True se o email for válido
        """
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))
