"""
Entidade de empresa.

Este módulo contém a entidade que representa uma empresa no sistema.
"""
from dataclasses import dataclass
from typing import Optional

from .base import Entity
from .dados_pessoais import Endereco


@dataclass
class Empresa(Entity):
    """
    Entidade que representa uma empresa.

    Uma empresa é uma organização que pode estar associada a um
    ou mais usuários do sistema.
    """

    razao_social: str
    nome_fantasia: str
    cnpj: str
    endereco: Endereco
    inscricao_estadual: Optional[str] = None
    inscricao_municipal: Optional[str] = None

    def atualizar_endereco(self, endereco: Endereco) -> None:
        """
        Atualiza o endereço da empresa.

        Args:
            endereco: Novo endereço
        """
        self.endereco = endereco
        self.atualizar()

    def formatar_documentos(self) -> str:
        """
        Retorna os documentos da empresa formatados como string.

        Returns:
            String formatada com os documentos da empresa
        """
        documentos = [
            f"CNPJ: {self.cnpj}",
            f"IE: {self.inscricao_estadual}" if self.inscricao_estadual else None,
            f"IM: {self.inscricao_municipal}" if self.inscricao_municipal else None,
        ]
        return " / ".join(d for d in documentos if d)
