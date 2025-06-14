"""
Serviço de domínio para produtos.

Este módulo contém o serviço de domínio que encapsula a lógica de negócio
relacionada a produtos que não pertence naturalmente a nenhuma entidade.
"""
from decimal import Decimal
from typing import List, Optional

from ..entities.produto import Produto, Variacao, Detalhe
from ..repositories.produto_repository import ProdutoRepository
from ...shared.value_objects.preco import Preco


class ProdutoService:
    """
    Serviço de domínio para produtos.

    Esta classe implementa a lógica de negócio relacionada a produtos
    que não pertence naturalmente a nenhuma entidade.
    """

    def __init__(self, produto_repository: ProdutoRepository):
        """
        Inicializa o serviço com suas dependências.

        Args:
            produto_repository: Repositório de produtos
        """
        self._repository = produto_repository

    def criar_produto(
        self,
        sku: str,
        nome: str,
        descricao: str,
        preco: Preco
    ) -> Produto:
        """
        Cria um novo produto.

        Args:
            sku: SKU do produto
            nome: Nome do produto
            descricao: Descrição do produto
            preco: Preço do produto

        Returns:
            Produto: O produto criado

        Raises:
            ValueError: Se o SKU já existe
        """
        if self._repository.buscar_por_sku(sku):
            raise ValueError(f"Já existe um produto com o SKU {sku}")

        produto = Produto(
            sku=sku,
            nome=nome,
            descricao=descricao,
            preco=preco
        )

        return self._repository.salvar(produto)

    def adicionar_variacao(
        self,
        produto_id: int,
        nome: str,
        descricao: str,
        codigo: str
    ) -> Optional[Produto]:
        """
        Adiciona uma variação a um produto.

        Args:
            produto_id: ID do produto
            nome: Nome da variação
            descricao: Descrição da variação
            codigo: Código da variação

        Returns:
            Optional[Produto]: O produto atualizado ou None se não encontrado
        """
        produto = self._repository.buscar_por_id(produto_id)
        if not produto:
            return None

        variacao = Variacao(
            nome=nome,
            descricao=descricao,
            codigo=codigo
        )

        produto.adicionar_variacao(variacao)
        return self._repository.atualizar(produto)

    def adicionar_detalhe(
        self,
        produto_id: int,
        nome: str,
        valor: str,
        tipo: str
    ) -> Optional[Produto]:
        """
        Adiciona um detalhe a um produto.

        Args:
            produto_id: ID do produto
            nome: Nome do detalhe
            valor: Valor do detalhe
            tipo: Tipo do detalhe

        Returns:
            Optional[Produto]: O produto atualizado ou None se não encontrado
        """
        produto = self._repository.buscar_por_id(produto_id)
        if not produto:
            return None

        detalhe = Detalhe(
            nome=nome,
            valor=valor,
            tipo=tipo
        )

        produto.adicionar_detalhe(detalhe)
        return self._repository.atualizar(produto)

    def atualizar_preco(
        self,
        produto_id: int,
        novo_preco: Preco
    ) -> Optional[Produto]:
        """
        Atualiza o preço de um produto.

        Args:
            produto_id: ID do produto
            novo_preco: Novo preço do produto

        Returns:
            Optional[Produto]: O produto atualizado ou None se não encontrado
        """
        produto = self._repository.buscar_por_id(produto_id)
        if not produto:
            return None

        produto.atualizar_preco(novo_preco)
        return self._repository.atualizar(produto)

    def buscar_por_faixa_de_preco(
        self,
        preco_minimo: Decimal,
        preco_maximo: Decimal
    ) -> List[Produto]:
        """
        Busca produtos por faixa de preço.

        Args:
            preco_minimo: Preço mínimo
            preco_maximo: Preço máximo

        Returns:
            List[Produto]: Lista de produtos na faixa de preço
        """
        return self._repository.buscar_por_faixa_de_preco(
            preco_minimo,
            preco_maximo
        )

    def desativar_produto(self, produto_id: int) -> bool:
        """
        Desativa um produto.

        Args:
            produto_id: ID do produto

        Returns:
            bool: True se desativado com sucesso, False caso contrário
        """
        produto = self._repository.buscar_por_id(produto_id)
        if not produto:
            return False

        produto.desativar()
        return self._repository.atualizar(produto) is not None

    def ativar_produto(self, produto_id: int) -> bool:
        """
        Ativa um produto.

        Args:
            produto_id: ID do produto

        Returns:
            bool: True se ativado com sucesso, False caso contrário
        """
        produto = self._repository.buscar_por_id(produto_id)
        if not produto:
            return False

        produto.ativar()
        return self._repository.atualizar(produto) is not None 