"""
Serviço de aplicação para produtos.

Este módulo contém o serviço de aplicação que coordena as operações
relacionadas a produtos, fazendo a ponte entre a interface com o usuário
e o domínio.
"""
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from ....domain.catalogo.entities.produto import Detalhe, Produto, Variacao
from ....domain.catalogo.repositories.produto_repository import ProdutoRepository
from ....domain.catalogo.services.produto_service import ProdutoService
from ....domain.shared.value_objects.moeda import Moeda
from ....domain.shared.value_objects.preco import Preco
from ..dtos.produto_dto import (
    AtualizarProdutoDTO,
    CriarProdutoDTO,
    DetalheDTO,
    ListagemProdutoDTO,
    PrecoDTO,
    ProdutoDTO,
    VariacaoDTO,
)


class ProdutoAppService:
    """
    Serviço de aplicação para produtos.

    Esta classe implementa os casos de uso relacionados a produtos,
    coordenando as operações entre a interface com o usuário e o domínio.
    """

    def __init__(self, produto_repository: ProdutoRepository):
        """
        Inicializa o serviço com suas dependências.

        Args:
            produto_repository: Repositório de produtos
        """
        self._repository = produto_repository
        self._service = ProdutoService(produto_repository)

    def criar_produto(self, dto: CriarProdutoDTO) -> ProdutoDTO:
        """
        Cria um novo produto.

        Args:
            dto: DTO com os dados do produto

        Returns:
            ProdutoDTO: DTO com os dados do produto criado

        Raises:
            ValueError: Se o SKU já existe
        """
        preco = Preco(
            valor=dto.preco_valor,
            moeda=Moeda(
                codigo=dto.preco_moeda,
                nome="",  # Nome será preenchido pelo construtor
                simbolo="",  # Símbolo será preenchido pelo construtor
            ),
        )

        produto = self._service.criar_produto(
            sku=dto.sku, nome=dto.nome, descricao=dto.descricao, preco=preco
        )

        return self._to_dto(produto)

    def atualizar_produto(
        self, produto_id: int, dto: AtualizarProdutoDTO
    ) -> Optional[ProdutoDTO]:
        """
        Atualiza um produto existente.

        Args:
            produto_id: ID do produto
            dto: DTO com os dados a serem atualizados

        Returns:
            Optional[ProdutoDTO]: DTO com os dados do produto atualizado
            ou None se não encontrado
        """
        produto = self._repository.buscar_por_id(produto_id)
        if not produto:
            return None

        if dto.nome is not None:
            produto.nome = dto.nome

        if dto.descricao is not None:
            produto.descricao = dto.descricao

        if dto.preco_valor is not None or dto.preco_moeda is not None:
            novo_preco = Preco(
                valor=dto.preco_valor or produto.preco.valor,
                moeda=Moeda(
                    codigo=dto.preco_moeda or produto.preco.moeda.codigo,
                    nome="",  # Nome será preenchido pelo construtor
                    simbolo="",  # Símbolo será preenchido pelo construtor
                ),
            )
            produto.atualizar_preco(novo_preco)

        produto = self._repository.atualizar(produto)
        return self._to_dto(produto)

    def buscar_por_id(self, produto_id: int) -> Optional[ProdutoDTO]:
        """
        Busca um produto pelo ID.

        Args:
            produto_id: ID do produto

        Returns:
            Optional[ProdutoDTO]: DTO com os dados do produto ou None
        """
        produto = self._repository.buscar_por_id(produto_id)
        if not produto:
            return None
        return self._to_dto(produto)

    def buscar_por_sku(self, sku: str) -> Optional[ProdutoDTO]:
        """
        Busca um produto pelo SKU.

        Args:
            sku: SKU do produto

        Returns:
            Optional[ProdutoDTO]: DTO com os dados do produto ou None
        """
        produto = self._repository.buscar_por_sku(sku)
        if not produto:
            return None
        return self._to_dto(produto)

    def listar(self, apenas_ativos: bool = True) -> List[ListagemProdutoDTO]:
        """
        Lista todos os produtos.

        Args:
            apenas_ativos: Se True, retorna apenas produtos ativos

        Returns:
            List[ListagemProdutoDTO]: Lista de DTOs com dados resumidos
            dos produtos
        """
        produtos = self._repository.listar(apenas_ativos)
        return [self._to_listagem_dto(p) for p in produtos]

    def buscar_por_faixa_de_preco(
        self, preco_minimo: Decimal, preco_maximo: Decimal
    ) -> List[ListagemProdutoDTO]:
        """
        Busca produtos por faixa de preço.

        Args:
            preco_minimo: Preço mínimo
            preco_maximo: Preço máximo

        Returns:
            List[ListagemProdutoDTO]: Lista de DTOs com dados resumidos
            dos produtos
        """
        produtos = self._service.buscar_por_faixa_de_preco(preco_minimo, preco_maximo)
        return [self._to_listagem_dto(p) for p in produtos]

    def desativar_produto(self, produto_id: int) -> bool:
        """
        Desativa um produto.

        Args:
            produto_id: ID do produto

        Returns:
            bool: True se desativado com sucesso, False caso contrário
        """
        return self._service.desativar_produto(produto_id)

    def ativar_produto(self, produto_id: int) -> bool:
        """
        Ativa um produto.

        Args:
            produto_id: ID do produto

        Returns:
            bool: True se ativado com sucesso, False caso contrário
        """
        return self._service.ativar_produto(produto_id)

    def _to_dto(self, produto: Produto) -> ProdutoDTO:
        """
        Converte uma entidade Produto para DTO.

        Args:
            produto: A entidade a ser convertida

        Returns:
            ProdutoDTO: O DTO correspondente
        """
        return ProdutoDTO(
            sku=produto.sku,
            nome=produto.nome,
            descricao=produto.descricao,
            preco=PrecoDTO(
                valor=produto.preco.valor,
                moeda=produto.preco.moeda.codigo,
                data_inicio=produto.preco.data_inicio,
                data_fim=produto.preco.data_fim,
            ),
            variacoes=[
                VariacaoDTO(
                    nome=v.nome,
                    descricao=v.descricao,
                    codigo=v.codigo,
                    detalhes=[
                        DetalheDTO(nome=d.nome, valor=d.valor, tipo=d.tipo)
                        for d in v.detalhes
                    ],
                )
                for v in produto.variacoes
            ],
            detalhes=[
                DetalheDTO(nome=d.nome, valor=d.valor, tipo=d.tipo)
                for d in produto.detalhes
            ],
        )

    def _to_listagem_dto(self, produto: Produto) -> ListagemProdutoDTO:
        """
        Converte uma entidade Produto para DTO de listagem.

        Args:
            produto: A entidade a ser convertida

        Returns:
            ListagemProdutoDTO: O DTO correspondente
        """
        return ListagemProdutoDTO(
            sku=produto.sku,
            nome=produto.nome,
            preco_valor=produto.preco.valor,
            preco_moeda=produto.preco.moeda.codigo,
            ativo=produto.ativo,
        )
