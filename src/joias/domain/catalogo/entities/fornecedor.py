"""
Entidade que representa um fornecedor.

Esta é uma entidade do domínio que representa um fornecedor de produtos,
com seus documentos, endereço e produtos fornecidos.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from ...shared.value_objects.endereco import Endereco
from .produto import Produto


@dataclass
class Documento:
    """
    Representa um documento de identificação.

    Este é um objeto de valor que encapsula os dados de um documento
    de identificação, como CNPJ, CPF, etc.
    """

    numero: str
    tipo: str

    def __post_init__(self):
        """Valida os dados do documento após a inicialização."""
        if not self.numero:
            raise ValueError("O número do documento não pode estar vazio")
        if not self.tipo:
            raise ValueError("O tipo do documento não pode estar vazio")

        # Remove caracteres não numéricos do número
        self.numero = "".join(filter(str.isdigit, self.numero))

        # Converte o tipo para maiúsculas
        self.tipo = self.tipo.upper()

        # Valida o tipo de documento
        if self.tipo == "CNPJ" and len(self.numero) != 14:
            raise ValueError("CNPJ deve ter 14 dígitos")
        elif self.tipo == "CPF" and len(self.numero) != 11:
            raise ValueError("CPF deve ter 11 dígitos")

    def __str__(self) -> str:
        """Retorna uma representação string do documento."""
        if self.tipo == "CNPJ":
            return f"CNPJ: {self._formatar_cnpj()}"
        elif self.tipo == "CPF":
            return f"CPF: {self._formatar_cpf()}"
        return f"{self.tipo}: {self.numero}"

    def _formatar_cnpj(self) -> str:
        """Formata o número como CNPJ: XX.XXX.XXX/XXXX-XX."""
        return f"{self.numero[:2]}.{self.numero[2:5]}.{self.numero[5:8]}/{self.numero[8:12]}-{self.numero[12:]}"

    def _formatar_cpf(self) -> str:
        """Formata o número como CPF: XXX.XXX.XXX-XX."""
        return (
            f"{self.numero[:3]}.{self.numero[3:6]}.{self.numero[6:9]}-{self.numero[9:]}"
        )


@dataclass
class Fornecedor:
    """
    Representa um fornecedor de produtos.

    Esta é uma entidade rica que encapsula toda a lógica relacionada
    a um fornecedor, incluindo seus documentos, endereço e produtos.
    """

    nome: str
    documentos: List[Documento]
    endereco: Endereco
    produtos: List[Produto] = field(default_factory=list)
    data_cadastro: datetime = field(default_factory=datetime.now)
    ativo: bool = True

    def __post_init__(self):
        """Valida os dados do fornecedor após a inicialização."""
        if not self.nome:
            raise ValueError("O nome não pode estar vazio")
        if not self.documentos:
            raise ValueError("O fornecedor deve ter pelo menos um documento")

    def adicionar_produto(self, produto: Produto) -> None:
        """
        Adiciona um produto à lista de produtos fornecidos.

        Args:
            produto: O produto a ser adicionado
        """
        if produto not in self.produtos:
            self.produtos.append(produto)

    def remover_produto(self, produto: Produto) -> None:
        """
        Remove um produto da lista de produtos fornecidos.

        Args:
            produto: O produto a ser removido
        """
        if produto in self.produtos:
            self.produtos.remove(produto)

    def listar_produtos(self) -> List[Produto]:
        """
        Lista todos os produtos fornecidos.

        Returns:
            List[Produto]: Lista de produtos
        """
        return self.produtos.copy()

    def desativar(self) -> None:
        """Desativa o fornecedor."""
        self.ativo = False

    def ativar(self) -> None:
        """Ativa o fornecedor."""
        self.ativo = True

    def atualizar_endereco(self, novo_endereco: Endereco) -> None:
        """
        Atualiza o endereço do fornecedor.

        Args:
            novo_endereco: O novo endereço
        """
        self.endereco = novo_endereco

    def adicionar_documento(self, documento: Documento) -> None:
        """
        Adiciona um novo documento ao fornecedor.

        Args:
            documento: O documento a ser adicionado
        """
        if documento not in self.documentos:
            self.documentos.append(documento)

    def remover_documento(self, documento: Documento) -> None:
        """
        Remove um documento do fornecedor.

        Args:
            documento: O documento a ser removido

        Raises:
            ValueError: Se for o último documento do fornecedor
        """
        if len(self.documentos) <= 1:
            raise ValueError("O fornecedor deve ter pelo menos um documento")
        if documento in self.documentos:
            self.documentos.remove(documento)

    def __str__(self) -> str:
        """Retorna uma representação string do fornecedor."""
        status = "ativo" if self.ativo else "inativo"
        documentos_str = ", ".join(str(doc) for doc in self.documentos)
        return f"{self.nome} ({status}) - Documentos: [{documentos_str}]"
