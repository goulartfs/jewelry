"""
Entidades de dados pessoais.

Este módulo contém as entidades relacionadas aos dados pessoais
de um indivíduo, como endereço e documentos.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from .base import Entity


@dataclass
class Endereco(Entity):
    """
    Entidade que representa um endereço físico.
    
    Um endereço é um local físico que pode estar associado
    a uma pessoa ou empresa.
    """
    logradouro: str
    numero: str
    bairro: str
    cidade: str
    estado: str
    cep: str
    complemento: Optional[str] = None
    pais: str = "Brasil"

    def formatar(self) -> str:
        """
        Retorna o endereço formatado como string.

        Returns:
            String formatada com o endereço completo
        """
        partes = [
            f"{self.logradouro}, {self.numero}",
            self.complemento if self.complemento else None,
            self.bairro,
            f"{self.cidade} - {self.estado}",
            f"CEP: {self.cep}",
            self.pais
        ]
        return ", ".join(p for p in partes if p)


@dataclass
class DadoPessoal(Entity):
    """
    Entidade que representa os dados pessoais de um indivíduo.
    
    Contém informações pessoais como nome, documentos e endereços
    associados à pessoa.
    """
    nome: str
    cpf: str
    data_nascimento: datetime
    rg: Optional[str] = None
    enderecos: List[Endereco] = field(default_factory=list)

    def adicionar_endereco(self, endereco: Endereco) -> None:
        """
        Adiciona um endereço aos dados pessoais.

        Args:
            endereco: Endereço a ser adicionado
        """
        self.enderecos.append(endereco)
        self.atualizar()

    def remover_endereco(self, endereco_id: int) -> None:
        """
        Remove um endereço dos dados pessoais.

        Args:
            endereco_id: ID do endereço a ser removido
        """
        self.enderecos = [
            e for e in self.enderecos
            if e.id != endereco_id
        ]
        self.atualizar()

    def obter_endereco_principal(self) -> Optional[Endereco]:
        """
        Retorna o primeiro endereço ativo da lista.

        Returns:
            O primeiro endereço ativo ou None se não houver endereços
        """
        enderecos_ativos = [e for e in self.enderecos if e.ativo]
        return enderecos_ativos[0] if enderecos_ativos else None 