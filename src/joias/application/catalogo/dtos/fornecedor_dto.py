"""
DTOs para fornecedores.

Este módulo contém os DTOs (Data Transfer Objects) usados para transferir
dados de fornecedores entre as camadas da aplicação.
"""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class EnderecoDTO:
    """DTO para endereços."""

    logradouro: str
    numero: str
    bairro: str
    cidade: str
    estado: str
    cep: str
    complemento: Optional[str] = None
    pais: str = "Brasil"


@dataclass
class DocumentoDTO:
    """DTO para documentos."""

    numero: str
    tipo: str


@dataclass
class FornecedorDTO:
    """DTO para fornecedores."""

    nome: str
    documentos: List[DocumentoDTO]
    endereco: EnderecoDTO
    ativo: bool


@dataclass
class CriarFornecedorDTO:
    """DTO para criação de fornecedores."""

    nome: str
    documento_numero: str
    documento_tipo: str
    endereco: EnderecoDTO


@dataclass
class AtualizarFornecedorDTO:
    """DTO para atualização de fornecedores."""

    nome: Optional[str] = None
    endereco: Optional[EnderecoDTO] = None


@dataclass
class ListagemFornecedorDTO:
    """DTO para listagem de fornecedores."""

    nome: str
    documento_principal: DocumentoDTO
    cidade: str
    estado: str
    ativo: bool
