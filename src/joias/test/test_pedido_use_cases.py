"""
Testes para os casos de uso de pedidos.

Este módulo contém os testes unitários para os casos de uso
relacionados a pedidos.
"""
import pytest
from datetime import datetime, timedelta
from decimal import Decimal

from ..domain.entities.pedido import Pedido, StatusPedido
from ..domain.entities.usuario import Usuario
from ..domain.entities.autorizacao import Perfil, Permissao
from ..domain.entities.dados_pessoais import DadoPessoal, Endereco
from ..domain.entities.produto import Produto, Preco
from ..application.use_cases.pedido import (
    CriarPedidoInput,
    CriarPedidoUseCase,
    AdicionarItemInput,
    AdicionarItemUseCase,
    AtualizarPedidoInput,
    AtualizarPedidoUseCase,
    AtualizarStatusInput,
    AtualizarStatusUseCase,
    ListarPedidosClienteUseCase,
    ListarPedidosAtivosUseCase
)
from ..infrastructure.repositories.memory.pedido import MemoryPedidoRepository
from ..infrastructure.repositories.memory.produto import MemoryProdutoRepository


@pytest.fixture
def pedido_repository():
    """Fixture que cria um repositório de pedidos em memória."""
    return MemoryPedidoRepository()


@pytest.fixture
def produto_repository():
    """Fixture que cria um repositório de produtos em memória."""
    return MemoryProdutoRepository()


@pytest.fixture
def endereco():
    """Fixture que cria um endereço."""
    return Endereco(
        logradouro="Rua Teste",
        numero="123",
        bairro="Centro",
        cidade="São Paulo",
        estado="SP",
        cep="01234-567"
    )


@pytest.fixture
def cliente(endereco):
    """Fixture que cria um cliente."""
    permissoes = [
        Permissao(nome="Criar Pedido", descricao="Pode criar pedidos", codigo="CRIAR_PEDIDO")
    ]
    perfil = Perfil(nome="Cliente", descricao="Perfil de cliente", permissoes=permissoes)
    dados_pessoais = DadoPessoal(
        nome="João Silva",
        cpf="123.456.789-00",
        data_nascimento=datetime(1990, 1, 1),
        enderecos=[endereco]
    )
    return Usuario(
        username="joao.silva",
        email="joao.silva@example.com",
        senha_hash="senha123",
        perfil=perfil,
        dados_pessoais=dados_pessoais
    )


@pytest.fixture
def produto():
    """Fixture que cria um produto."""
    return Produto(
        nome="Anel Solitário",
        descricao="Anel solitário em ouro 18k",
        codigo="ANL-001",
        preco=Preco(valor=Decimal("1000.00"))
    )


def test_criar_pedido(pedido_repository, cliente, endereco):
    """Testa a criação de um pedido."""
    use_case = CriarPedidoUseCase(pedido_repository)
    input_data = CriarPedidoInput(
        cliente=cliente,
        endereco_entrega=endereco,
        observacoes="Entregar no período da tarde"
    )

    pedido = use_case.execute(input_data)

    assert pedido.id is not None
    assert pedido.cliente == cliente
    assert pedido.endereco_entrega == endereco
    assert pedido.status == StatusPedido.RASCUNHO


def test_adicionar_item(pedido_repository, produto_repository, cliente, produto):
    """Testa a adição de um item ao pedido."""
    # Cria um pedido
    criar_pedido_use_case = CriarPedidoUseCase(pedido_repository)
    pedido = criar_pedido_use_case.execute(CriarPedidoInput(cliente=cliente))

    # Adiciona o produto ao repositório
    produto = produto_repository.criar(produto)

    # Adiciona um item ao pedido
    adicionar_item_use_case = AdicionarItemUseCase(pedido_repository, produto_repository)
    pedido_atualizado = adicionar_item_use_case.execute(AdicionarItemInput(
        pedido_id=pedido.id,
        produto_id=produto.id,
        quantidade=1
    ))

    assert len(pedido_atualizado.itens) == 1
    assert pedido_atualizado.itens[0].produto == produto
    assert pedido_atualizado.itens[0].quantidade == 1
    assert pedido_atualizado.itens[0].preco_unitario == produto.preco.valor


def test_atualizar_pedido(pedido_repository, cliente, endereco):
    """Testa a atualização de um pedido."""
    # Cria um pedido
    criar_use_case = CriarPedidoUseCase(pedido_repository)
    pedido = criar_use_case.execute(CriarPedidoInput(cliente=cliente))

    # Atualiza o pedido
    atualizar_use_case = AtualizarPedidoUseCase(pedido_repository)
    pedido_atualizado = atualizar_use_case.execute(AtualizarPedidoInput(
        id=pedido.id,
        endereco_entrega=endereco,
        observacoes="Entregar no período da tarde"
    ))

    assert pedido_atualizado.endereco_entrega == endereco
    assert pedido_atualizado.observacoes == "Entregar no período da tarde"


def test_atualizar_status(pedido_repository, cliente):
    """Testa a atualização do status de um pedido."""
    # Cria um pedido
    criar_use_case = CriarPedidoUseCase(pedido_repository)
    pedido = criar_use_case.execute(CriarPedidoInput(cliente=cliente))

    # Atualiza o status do pedido
    atualizar_use_case = AtualizarStatusUseCase(pedido_repository)
    pedido_atualizado = atualizar_use_case.execute(AtualizarStatusInput(
        pedido_id=pedido.id,
        novo_status=StatusPedido.AGUARDANDO_PAGAMENTO
    ))

    assert pedido_atualizado.status == StatusPedido.AGUARDANDO_PAGAMENTO


def test_listar_pedidos_cliente(pedido_repository, cliente):
    """Testa a listagem de pedidos de um cliente."""
    # Cria alguns pedidos
    criar_use_case = CriarPedidoUseCase(pedido_repository)
    
    # Pedido 1
    criar_use_case.execute(CriarPedidoInput(cliente=cliente))

    # Pedido 2
    criar_use_case.execute(CriarPedidoInput(cliente=cliente))

    # Lista os pedidos do cliente
    listar_use_case = ListarPedidosClienteUseCase(pedido_repository)
    pedidos = listar_use_case.execute(cliente.id)

    assert len(pedidos) == 2
    assert all(p.cliente.id == cliente.id for p in pedidos)


def test_listar_pedidos_ativos(pedido_repository, cliente):
    """Testa a listagem de pedidos ativos."""
    # Cria alguns pedidos
    criar_use_case = CriarPedidoUseCase(pedido_repository)
    atualizar_status_use_case = AtualizarStatusUseCase(pedido_repository)
    
    # Pedido 1 - Ativo (AGUARDANDO_PAGAMENTO)
    pedido1 = criar_use_case.execute(CriarPedidoInput(cliente=cliente))
    atualizar_status_use_case.execute(AtualizarStatusInput(
        pedido_id=pedido1.id,
        novo_status=StatusPedido.AGUARDANDO_PAGAMENTO
    ))

    # Pedido 2 - Ativo (EM_PRODUCAO)
    pedido2 = criar_use_case.execute(CriarPedidoInput(cliente=cliente))
    atualizar_status_use_case.execute(AtualizarStatusInput(
        pedido_id=pedido2.id,
        novo_status=StatusPedido.EM_PRODUCAO
    ))

    # Pedido 3 - Inativo (ENTREGUE)
    pedido3 = criar_use_case.execute(CriarPedidoInput(cliente=cliente))
    atualizar_status_use_case.execute(AtualizarStatusInput(
        pedido_id=pedido3.id,
        novo_status=StatusPedido.ENTREGUE
    ))

    # Lista os pedidos ativos
    listar_use_case = ListarPedidosAtivosUseCase(pedido_repository)
    pedidos = listar_use_case.execute()

    assert len(pedidos) == 2
    assert all(p.status not in {StatusPedido.CANCELADO, StatusPedido.ENTREGUE} for p in pedidos) 