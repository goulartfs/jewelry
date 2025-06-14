"""
Mapeador entre entidades de domínio e modelos SQLAlchemy para produtos.

Este módulo é responsável por converter entre as entidades de domínio
e os modelos SQLAlchemy para produtos.
"""
from decimal import Decimal
from datetime import datetime

from .....domain.catalogo.entities.produto import Produto, Variacao, Detalhe
from .....domain.shared.value_objects.preco import Preco
from .....domain.shared.value_objects.moeda import Moeda
from ..models.produto import (
    ProdutoModel,
    VariacaoModel,
    DetalheModel,
    DetalheVariacaoModel
)


class ProdutoMapper:
    """
    Mapeador entre entidades de domínio e modelos SQLAlchemy para produtos.

    Esta classe é responsável por converter entre as entidades de domínio
    e os modelos SQLAlchemy para produtos.
    """

    def to_model(self, entity: Produto) -> ProdutoModel:
        """
        Converte uma entidade Produto para um modelo SQLAlchemy.

        Args:
            entity: A entidade a ser convertida

        Returns:
            ProdutoModel: O modelo SQLAlchemy correspondente
        """
        model = ProdutoModel(
            sku=entity.sku,
            nome=entity.nome,
            descricao=entity.descricao,
            preco_valor=entity.preco.valor,
            preco_moeda=entity.preco.moeda.codigo,
            preco_data_inicio=entity.preco.data_inicio,
            preco_data_fim=entity.preco.data_fim,
            data_criacao=entity.data_criacao,
            ativo=entity.ativo
        )

        # Converte variações
        model.variacoes = [
            self._variacao_to_model(v, model)
            for v in entity.variacoes
        ]

        # Converte detalhes
        model.detalhes = [
            self._detalhe_to_model(d, model)
            for d in entity.detalhes
        ]

        return model

    def to_entity(self, model: ProdutoModel) -> Produto:
        """
        Converte um modelo SQLAlchemy para uma entidade Produto.

        Args:
            model: O modelo a ser convertido

        Returns:
            Produto: A entidade correspondente
        """
        # Cria o objeto Preco
        preco = Preco(
            valor=model.preco_valor,
            moeda=Moeda(
                codigo=model.preco_moeda,
                nome="",  # Nome será preenchido pelo construtor
                simbolo=""  # Símbolo será preenchido pelo construtor
            ),
            data_inicio=model.preco_data_inicio,
            data_fim=model.preco_data_fim
        )

        # Converte variações
        variacoes = [
            self._variacao_to_entity(v)
            for v in model.variacoes
        ]

        # Converte detalhes
        detalhes = [
            self._detalhe_to_entity(d)
            for d in model.detalhes
        ]

        return Produto(
            sku=model.sku,
            nome=model.nome,
            descricao=model.descricao,
            preco=preco,
            variacoes=variacoes,
            detalhes=detalhes,
            data_criacao=model.data_criacao,
            ativo=model.ativo
        )

    def _variacao_to_model(
        self,
        entity: Variacao,
        produto_model: ProdutoModel
    ) -> VariacaoModel:
        """
        Converte uma entidade Variacao para um modelo SQLAlchemy.

        Args:
            entity: A entidade a ser convertida
            produto_model: O modelo do produto pai

        Returns:
            VariacaoModel: O modelo SQLAlchemy correspondente
        """
        model = VariacaoModel(
            nome=entity.nome,
            descricao=entity.descricao,
            codigo=entity.codigo,
            data_criacao=entity.data_criacao,
            ativo=entity.ativo,
            produto=produto_model
        )

        # Converte detalhes da variação
        model.detalhes = [
            self._detalhe_variacao_to_model(d, model)
            for d in entity.detalhes
        ]

        return model

    def _variacao_to_entity(self, model: VariacaoModel) -> Variacao:
        """
        Converte um modelo SQLAlchemy para uma entidade Variacao.

        Args:
            model: O modelo a ser convertido

        Returns:
            Variacao: A entidade correspondente
        """
        # Converte detalhes da variação
        detalhes = [
            self._detalhe_to_entity(d)
            for d in model.detalhes
        ]

        return Variacao(
            nome=model.nome,
            descricao=model.descricao,
            codigo=model.codigo,
            detalhes=detalhes,
            data_criacao=model.data_criacao,
            ativo=model.ativo
        )

    def _detalhe_to_model(
        self,
        entity: Detalhe,
        produto_model: ProdutoModel
    ) -> DetalheModel:
        """
        Converte uma entidade Detalhe para um modelo SQLAlchemy.

        Args:
            entity: A entidade a ser convertida
            produto_model: O modelo do produto pai

        Returns:
            DetalheModel: O modelo SQLAlchemy correspondente
        """
        return DetalheModel(
            nome=entity.nome,
            valor=entity.valor,
            tipo=entity.tipo,
            data_criacao=entity.data_criacao,
            ativo=entity.ativo,
            produto=produto_model
        )

    def _detalhe_variacao_to_model(
        self,
        entity: Detalhe,
        variacao_model: VariacaoModel
    ) -> DetalheVariacaoModel:
        """
        Converte uma entidade Detalhe para um modelo SQLAlchemy de detalhe de variação.

        Args:
            entity: A entidade a ser convertida
            variacao_model: O modelo da variação pai

        Returns:
            DetalheVariacaoModel: O modelo SQLAlchemy correspondente
        """
        return DetalheVariacaoModel(
            nome=entity.nome,
            valor=entity.valor,
            tipo=entity.tipo,
            data_criacao=entity.data_criacao,
            ativo=entity.ativo,
            variacao=variacao_model
        )

    def _detalhe_to_entity(
        self,
        model: DetalheModel | DetalheVariacaoModel
    ) -> Detalhe:
        """
        Converte um modelo SQLAlchemy para uma entidade Detalhe.

        Args:
            model: O modelo a ser convertido

        Returns:
            Detalhe: A entidade correspondente
        """
        return Detalhe(
            nome=model.nome,
            valor=model.valor,
            tipo=model.tipo,
            data_criacao=model.data_criacao,
            ativo=model.ativo
        ) 