"""
Interface do repositório de fornecedores.

Este módulo define a interface que deve ser implementada por qualquer
repositório que queira persistir fornecedores.
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.fornecedor import Fornecedor, Documento


class FornecedorRepository(ABC):
    """
    Interface para repositório de fornecedores.

    Esta é uma interface que define os métodos que devem ser implementados
    por qualquer repositório que queira persistir fornecedores, seguindo o
    princípio de inversão de dependência do SOLID.
    """

    @abstractmethod
    def salvar(self, fornecedor: Fornecedor) -> Fornecedor:
        """
        Salva um fornecedor no repositório.

        Args:
            fornecedor: O fornecedor a ser salvo

        Returns:
            Fornecedor: O fornecedor salvo com ID atualizado
        """
        pass

    @abstractmethod
    def buscar_por_id(self, fornecedor_id: int) -> Optional[Fornecedor]:
        """
        Busca um fornecedor pelo ID.

        Args:
            fornecedor_id: ID do fornecedor

        Returns:
            Optional[Fornecedor]: O fornecedor encontrado ou None
        """
        pass

    @abstractmethod
    def buscar_por_documento(self, documento: Documento) -> Optional[Fornecedor]:
        """
        Busca um fornecedor pelo documento.

        Args:
            documento: Documento do fornecedor

        Returns:
            Optional[Fornecedor]: O fornecedor encontrado ou None
        """
        pass

    @abstractmethod
    def listar(self, apenas_ativos: bool = True) -> List[Fornecedor]:
        """
        Lista todos os fornecedores.

        Args:
            apenas_ativos: Se True, retorna apenas fornecedores ativos

        Returns:
            List[Fornecedor]: Lista de fornecedores
        """
        pass

    @abstractmethod
    def buscar_por_nome(self, nome: str) -> List[Fornecedor]:
        """
        Busca fornecedores por nome.

        Args:
            nome: Nome ou parte do nome do fornecedor

        Returns:
            List[Fornecedor]: Lista de fornecedores encontrados
        """
        pass

    @abstractmethod
    def atualizar(self, fornecedor: Fornecedor) -> Optional[Fornecedor]:
        """
        Atualiza um fornecedor existente.

        Args:
            fornecedor: O fornecedor com dados atualizados

        Returns:
            Optional[Fornecedor]: O fornecedor atualizado ou None se não encontrado
        """
        pass

    @abstractmethod
    def excluir(self, fornecedor_id: int) -> bool:
        """
        Remove um fornecedor.

        Args:
            fornecedor_id: ID do fornecedor

        Returns:
            bool: True se removido com sucesso, False caso contrário
        """
        pass 