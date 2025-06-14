"""
Objeto de valor que representa um endereço.

Este é um objeto de valor compartilhado que pode ser usado em diferentes
contextos do sistema, como endereço de entrega, endereço de cobrança, etc.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Endereco:
    """
    Representa um endereço físico.

    Este é um objeto de valor imutável que encapsula todos os dados
    necessários para representar um endereço físico completo.
    """

    logradouro: str
    numero: str
    bairro: str
    cidade: str
    estado: str
    cep: str
    complemento: Optional[str] = None
    pais: str = "Brasil"

    def __post_init__(self):
        """Valida os dados do endereço após a inicialização."""
        if not self.logradouro:
            raise ValueError("O logradouro não pode estar vazio")
        if not self.numero:
            raise ValueError("O número não pode estar vazio")
        if not self.bairro:
            raise ValueError("O bairro não pode estar vazio")
        if not self.cidade:
            raise ValueError("A cidade não pode estar vazia")
        if not self.estado:
            raise ValueError("O estado não pode estar vazio")
        if not self.cep:
            raise ValueError("O CEP não pode estar vazio")

        # Remove espaços extras e formata o CEP
        object.__setattr__(self, "cep", self._formatar_cep(self.cep))

        # Garante que estado está em maiúsculas
        object.__setattr__(self, "estado", self.estado.upper())

    def _formatar_cep(self, cep: str) -> str:
        """
        Formata o CEP removendo caracteres não numéricos.

        Args:
            cep: O CEP a ser formatado

        Returns:
            str: O CEP formatado

        Raises:
            ValueError: Se o CEP não tiver 8 dígitos após a formatação
        """
        # Remove todos os caracteres não numéricos
        cep_limpo = "".join(filter(str.isdigit, cep))

        if len(cep_limpo) != 8:
            raise ValueError("O CEP deve ter 8 dígitos")

        # Formata o CEP como XXXXX-XXX
        return f"{cep_limpo[:5]}-{cep_limpo[5:]}"

    def __str__(self) -> str:
        """Retorna uma representação string do endereço."""
        partes = [
            f"{self.logradouro}, {self.numero}",
            self.complemento if self.complemento else None,
            self.bairro,
            f"{self.cidade}/{self.estado}",
            self.cep,
            self.pais if self.pais != "Brasil" else None,
        ]
        return ", ".join(p for p in partes if p)
