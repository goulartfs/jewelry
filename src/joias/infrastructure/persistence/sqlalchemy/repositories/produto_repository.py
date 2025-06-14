"""
Implementação do repositório de produtos usando SQLAlchemy.

Este módulo implementa a interface ProdutoRepository usando SQLAlchemy
como tecnologia de persistência.
"""
from decimal import Decimal
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from .....domain.catalogo.entities.produto import Produto
from .....domain.catalogo.repositories.produto_repository import ProdutoRepository
from ..models.produto import ProdutoModel
from ..mappers.produto_mapper import ProdutoMapper


class SQLAlchemyProdutoRepository(ProdutoRepository):
    """
    Implementação do repositório de produtos usando SQLAlchemy.

    Esta classe implementa a interface ProdutoRepository usando SQLAlchemy
    como tecnologia de persistência.
    """

    def __init__(self, session: Session):
        """
        Inicializa o repositório com uma sessão do SQLAlchemy.

        Args:
            session: Sessão do SQLAlchemy
        """
        self._session = session
        self._mapper = ProdutoMapper()

    def salvar(self, produto: Produto) -> Produto:
        """
        Salva um produto no banco de dados.

        Args:
            produto: O produto a ser salvo

        Returns:
            Produto: O produto salvo com ID atualizado
        """
        model = self._mapper.to_model(produto)
        self._session.add(model)
        self._session.commit()
        return self._mapper.to_entity(model)

    def buscar_por_id(self, produto_id: int) -> Optional[Produto]:
        """
        Busca um produto pelo ID.

        Args:
            produto_id: ID do produto

        Returns:
            Optional[Produto]: O produto encontrado ou None
        """
        model = self._session.query(ProdutoModel).get(produto_id)
        if not model:
            return None
        return self._mapper.to_entity(model)

    def buscar_por_sku(self, sku: str) -> Optional[Produto]:
        """
        Busca um produto pelo SKU.

        Args:
            sku: SKU do produto

        Returns:
            Optional[Produto]: O produto encontrado ou None
        """
        model = (
            self._session.query(ProdutoModel)
            .filter(ProdutoModel.sku == sku)
            .first()
        )
        if not model:
            return None
        return self._mapper.to_entity(model)

    def listar(self, apenas_ativos: bool = True) -> List[Produto]:
        """
        Lista todos os produtos.

        Args:
            apenas_ativos: Se True, retorna apenas produtos ativos

        Returns:
            List[Produto]: Lista de produtos
        """
        query = self._session.query(ProdutoModel)
        if apenas_ativos:
            query = query.filter(ProdutoModel.ativo == True)
        return [self._mapper.to_entity(model) for model in query.all()]

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
        models = (
            self._session.query(ProdutoModel)
            .filter(
                and_(
                    ProdutoModel.preco_valor >= preco_minimo,
                    ProdutoModel.preco_valor <= preco_maximo,
                    ProdutoModel.ativo == True
                )
            )
            .all()
        )
        return [self._mapper.to_entity(model) for model in models]

    def atualizar(self, produto: Produto) -> Optional[Produto]:
        """
        Atualiza um produto existente.

        Args:
            produto: O produto com dados atualizados

        Returns:
            Optional[Produto]: O produto atualizado ou None se não encontrado
        """
        model = self._session.query(ProdutoModel).get(produto.id)
        if not model:
            return None

        updated_model = self._mapper.to_model(produto)
        for key, value in updated_model.__dict__.items():
            if not key.startswith('_'):
                setattr(model, key, value)

        self._session.commit()
        return self._mapper.to_entity(model)

    def excluir(self, produto_id: int) -> bool:
        """
        Remove um produto.

        Args:
            produto_id: ID do produto

        Returns:
            bool: True se removido com sucesso, False caso contrário
        """
        model = self._session.query(ProdutoModel).get(produto_id)
        if not model:
            return False

        self._session.delete(model)
        self._session.commit()
        return True 