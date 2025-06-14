"""
Serviço de domínio para fornecedores.

Este módulo contém o serviço de domínio que encapsula a lógica de negócio
relacionada a fornecedores que não pertence naturalmente a nenhuma entidade.
"""
from typing import List, Optional

from ..entities.fornecedor import Fornecedor, Documento
from ..repositories.fornecedor_repository import FornecedorRepository
from ...shared.value_objects.endereco import Endereco


class FornecedorService:
    """
    Serviço de domínio para fornecedores.

    Esta classe implementa a lógica de negócio relacionada a fornecedores
    que não pertence naturalmente a nenhuma entidade.
    """

    def __init__(self, fornecedor_repository: FornecedorRepository):
        """
        Inicializa o serviço com suas dependências.

        Args:
            fornecedor_repository: Repositório de fornecedores
        """
        self._repository = fornecedor_repository

    def criar_fornecedor(
        self,
        nome: str,
        documento: Documento,
        endereco: Endereco
    ) -> Fornecedor:
        """
        Cria um novo fornecedor.

        Args:
            nome: Nome do fornecedor
            documento: Documento principal do fornecedor
            endereco: Endereço do fornecedor

        Returns:
            Fornecedor: O fornecedor criado

        Raises:
            ValueError: Se já existe um fornecedor com o mesmo documento
        """
        # Verifica se já existe um fornecedor com o mesmo documento
        if self._repository.buscar_por_documento(documento):
            raise ValueError(
                f"Já existe um fornecedor com o documento {documento}"
            )

        fornecedor = Fornecedor(
            nome=nome,
            documentos=[documento],
            endereco=endereco
        )

        return self._repository.salvar(fornecedor)

    def adicionar_documento(
        self,
        fornecedor_id: int,
        documento: Documento
    ) -> Optional[Fornecedor]:
        """
        Adiciona um novo documento a um fornecedor.

        Args:
            fornecedor_id: ID do fornecedor
            documento: Documento a ser adicionado

        Returns:
            Optional[Fornecedor]: O fornecedor atualizado ou None se não encontrado

        Raises:
            ValueError: Se já existe um fornecedor com o mesmo documento
        """
        # Verifica se já existe um fornecedor com o mesmo documento
        if self._repository.buscar_por_documento(documento):
            raise ValueError(
                f"Já existe um fornecedor com o documento {documento}"
            )

        fornecedor = self._repository.buscar_por_id(fornecedor_id)
        if not fornecedor:
            return None

        fornecedor.adicionar_documento(documento)
        return self._repository.atualizar(fornecedor)

    def remover_documento(
        self,
        fornecedor_id: int,
        documento: Documento
    ) -> Optional[Fornecedor]:
        """
        Remove um documento de um fornecedor.

        Args:
            fornecedor_id: ID do fornecedor
            documento: Documento a ser removido

        Returns:
            Optional[Fornecedor]: O fornecedor atualizado ou None se não encontrado

        Raises:
            ValueError: Se for o último documento do fornecedor
        """
        fornecedor = self._repository.buscar_por_id(fornecedor_id)
        if not fornecedor:
            return None

        fornecedor.remover_documento(documento)
        return self._repository.atualizar(fornecedor)

    def atualizar_endereco(
        self,
        fornecedor_id: int,
        novo_endereco: Endereco
    ) -> Optional[Fornecedor]:
        """
        Atualiza o endereço de um fornecedor.

        Args:
            fornecedor_id: ID do fornecedor
            novo_endereco: Novo endereço

        Returns:
            Optional[Fornecedor]: O fornecedor atualizado ou None se não encontrado
        """
        fornecedor = self._repository.buscar_por_id(fornecedor_id)
        if not fornecedor:
            return None

        fornecedor.atualizar_endereco(novo_endereco)
        return self._repository.atualizar(fornecedor)

    def buscar_por_nome(self, nome: str) -> List[Fornecedor]:
        """
        Busca fornecedores por nome.

        Args:
            nome: Nome ou parte do nome do fornecedor

        Returns:
            List[Fornecedor]: Lista de fornecedores encontrados
        """
        return self._repository.buscar_por_nome(nome)

    def desativar_fornecedor(self, fornecedor_id: int) -> bool:
        """
        Desativa um fornecedor.

        Args:
            fornecedor_id: ID do fornecedor

        Returns:
            bool: True se desativado com sucesso, False caso contrário
        """
        fornecedor = self._repository.buscar_por_id(fornecedor_id)
        if not fornecedor:
            return False

        fornecedor.desativar()
        return self._repository.atualizar(fornecedor) is not None

    def ativar_fornecedor(self, fornecedor_id: int) -> bool:
        """
        Ativa um fornecedor.

        Args:
            fornecedor_id: ID do fornecedor

        Returns:
            bool: True se ativado com sucesso, False caso contrário
        """
        fornecedor = self._repository.buscar_por_id(fornecedor_id)
        if not fornecedor:
            return False

        fornecedor.ativar()
        return self._repository.atualizar(fornecedor) is not None 