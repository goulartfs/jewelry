"""
Casos de uso relacionados a pedidos.

Este módulo contém os casos de uso para operações
relacionadas a pedidos.
"""
from dataclasses import dataclass
from decimal import Decimal
from typing import List, Optional

from ...domain.entities.pedido import Pedido, ItemPedido, StatusPedido
from ...domain.entities.produto import Produto, Variacao
from ...domain.entities.usuario import Usuario
from ...domain.entities.dados_pessoais import Endereco
from ...domain.repositories.pedido import PedidoRepository
from ...domain.repositories.produto import ProdutoRepository
from .base import UseCase


@dataclass
class CriarPedidoInput:
    """Dados de entrada para criação de pedido."""
    cliente: Usuario
    endereco_entrega: Optional[Endereco] = None
    observacoes: Optional[str] = None


class CriarPedidoUseCase(UseCase[CriarPedidoInput, Pedido]):
    """Caso de uso para criar um novo pedido."""

    def __init__(self, pedido_repository: PedidoRepository):
        self.pedido_repository = pedido_repository

    def execute(self, input_data: CriarPedidoInput) -> Pedido:
        """
        Executa o caso de uso.

        Args:
            input_data: Dados de entrada

        Returns:
            Pedido criado
        """
        pedido = Pedido(
            cliente=input_data.cliente,
            endereco_entrega=input_data.endereco_entrega,
            observacoes=input_data.observacoes
        )

        return self.pedido_repository.criar(pedido)


@dataclass
class AdicionarItemInput:
    """Dados de entrada para adicionar item ao pedido."""
    pedido_id: int
    produto_id: int
    quantidade: int
    variacao_id: Optional[int] = None
    desconto: Decimal = Decimal("0")


class AdicionarItemUseCase(UseCase[AdicionarItemInput, Pedido]):
    """Caso de uso para adicionar um item a um pedido."""

    def __init__(
        self,
        pedido_repository: PedidoRepository,
        produto_repository: ProdutoRepository
    ):
        self.pedido_repository = pedido_repository
        self.produto_repository = produto_repository

    def execute(self, input_data: AdicionarItemInput) -> Pedido:
        """
        Executa o caso de uso.

        Args:
            input_data: Dados de entrada

        Returns:
            Pedido atualizado

        Raises:
            ValueError: Se o pedido ou produto não existirem
        """
        pedido = self.pedido_repository.buscar_por_id(input_data.pedido_id)
        if not pedido:
            raise ValueError("Pedido não encontrado")

        if not pedido.pode_modificar():
            raise ValueError("Pedido não pode ser modificado")

        produto = self.produto_repository.buscar_por_id(input_data.produto_id)
        if not produto:
            raise ValueError("Produto não encontrado")

        variacao = None
        if input_data.variacao_id:
            variacao = next(
                (v for v in produto.variacoes if v.id == input_data.variacao_id),
                None
            )
            if not variacao:
                raise ValueError("Variação não encontrada")

        item = ItemPedido(
            produto=produto,
            quantidade=input_data.quantidade,
            preco_unitario=produto.preco.valor,
            variacao=variacao,
            desconto=input_data.desconto
        )

        pedido.adicionar_item(item)
        return self.pedido_repository.atualizar(pedido)


@dataclass
class AtualizarPedidoInput:
    """Dados de entrada para atualização de pedido."""
    id: int
    endereco_entrega: Optional[Endereco] = None
    observacoes: Optional[str] = None
    desconto_total: Optional[Decimal] = None


class AtualizarPedidoUseCase(UseCase[AtualizarPedidoInput, Pedido]):
    """Caso de uso para atualizar um pedido existente."""

    def __init__(self, pedido_repository: PedidoRepository):
        self.pedido_repository = pedido_repository

    def execute(self, input_data: AtualizarPedidoInput) -> Pedido:
        """
        Executa o caso de uso.

        Args:
            input_data: Dados de entrada

        Returns:
            Pedido atualizado

        Raises:
            ValueError: Se o pedido não existir ou não puder ser modificado
        """
        pedido = self.pedido_repository.buscar_por_id(input_data.id)
        if not pedido:
            raise ValueError("Pedido não encontrado")

        if not pedido.pode_modificar():
            raise ValueError("Pedido não pode ser modificado")

        if input_data.endereco_entrega:
            pedido.definir_endereco_entrega(input_data.endereco_entrega)
        if input_data.observacoes is not None:
            pedido.observacoes = input_data.observacoes
        if input_data.desconto_total is not None:
            pedido.desconto_total = input_data.desconto_total

        return self.pedido_repository.atualizar(pedido)


@dataclass
class AtualizarStatusInput:
    """Dados de entrada para atualização de status do pedido."""
    pedido_id: int
    novo_status: StatusPedido


class AtualizarStatusUseCase(UseCase[AtualizarStatusInput, Pedido]):
    """Caso de uso para atualizar o status de um pedido."""

    def __init__(self, pedido_repository: PedidoRepository):
        self.pedido_repository = pedido_repository

    def execute(self, input_data: AtualizarStatusInput) -> Pedido:
        """
        Executa o caso de uso.

        Args:
            input_data: Dados de entrada

        Returns:
            Pedido atualizado

        Raises:
            ValueError: Se o pedido não existir
        """
        pedido = self.pedido_repository.buscar_por_id(input_data.pedido_id)
        if not pedido:
            raise ValueError("Pedido não encontrado")

        pedido.atualizar_status(input_data.novo_status)
        return self.pedido_repository.atualizar(pedido)


class ListarPedidosClienteUseCase(UseCase[int, List[Pedido]]):
    """Caso de uso para listar pedidos de um cliente."""

    def __init__(self, pedido_repository: PedidoRepository):
        self.pedido_repository = pedido_repository

    def execute(self, cliente_id: int) -> List[Pedido]:
        """
        Executa o caso de uso.

        Args:
            cliente_id: ID do cliente

        Returns:
            Lista de pedidos do cliente
        """
        return self.pedido_repository.buscar_por_cliente(cliente_id)


class ListarPedidosAtivosUseCase(UseCase[None, List[Pedido]]):
    """Caso de uso para listar pedidos ativos."""

    def __init__(self, pedido_repository: PedidoRepository):
        self.pedido_repository = pedido_repository

    def execute(self, _: None = None) -> List[Pedido]:
        """
        Executa o caso de uso.

        Returns:
            Lista de pedidos ativos
        """
        return self.pedido_repository.buscar_pedidos_ativos() 