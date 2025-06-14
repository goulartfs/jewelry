"""
Testes para o serviço de Pedido.
"""
import pytest
from datetime import datetime, timedelta
from domain.pedido.models import Pedido, ItemPedido
from domain.pedido.service import PedidoService
from domain.catalogo.service import CatalogoService
from domain.catalogo.models import Produto, Catalogo

@pytest.fixture
def catalogo_service():
    return CatalogoService()

@pytest.fixture
def pedido_service(catalogo_service):
    return PedidoService(catalogo_service)

@pytest.fixture
def produto_exemplo():
    return Produto(
        id=1,
        nome="Anel Esmeralda",
        descricao="Anel banhado a ouro com pedra esmeralda",
        tamanho_do_pacote=10,
        preco_do_pacote=100.0,
        quantidade_minima_por_pedido=3
    )

@pytest.fixture
def catalogo_exemplo(catalogo_service, produto_exemplo):
    catalogo = catalogo_service.criar_catalogo(
        nome="Catálogo Teste",
        fornecedor="Joias & Cia",
        data_inicio=datetime.now(),
        data_fim=datetime.now() + timedelta(days=30)
    )
    catalogo_service.adicionar_produto(catalogo.id, produto_exemplo)
    return catalogo

def test_criar_pedido(pedido_service, catalogo_exemplo):
    """Deve criar um pedido com sucesso."""
    pedido = pedido_service.criar_pedido(catalogo_exemplo.id)
    
    assert pedido is not None
    assert pedido.catalogo_id == catalogo_exemplo.id
    assert pedido.status == "aberto"
    assert len(pedido.itens) == 0

def test_adicionar_item_pedido(pedido_service, catalogo_exemplo, produto_exemplo):
    """Deve adicionar um item ao pedido com sucesso."""
    pedido = pedido_service.criar_pedido(catalogo_exemplo.id)
    
    item = pedido_service.adicionar_item(
        pedido_id=pedido.id,
        produto_id=produto_exemplo.id,
        quantidade=5,
        comprador="Maria"
    )
    
    assert item is not None
    assert item.produto.id == produto_exemplo.id
    assert item.quantidade == 5
    assert item.comprador == "Maria"
    
    pedido_atualizado = pedido_service.buscar_pedido(pedido.id)
    assert len(pedido_atualizado.itens) == 1

def test_fechar_pedido(pedido_service, catalogo_exemplo, produto_exemplo):
    """Deve fechar um pedido com sucesso."""
    pedido = pedido_service.criar_pedido(catalogo_exemplo.id)
    
    pedido_service.adicionar_item(
        pedido_id=pedido.id,
        produto_id=produto_exemplo.id,
        quantidade=5,
        comprador="Maria"
    )
    
    pedido_fechado = pedido_service.fechar_pedido(pedido.id)
    
    assert pedido_fechado.status == "fechado"

def test_processar_pedido(pedido_service, catalogo_exemplo, produto_exemplo):
    """Deve processar um pedido fechado com sucesso."""
    pedido = pedido_service.criar_pedido(catalogo_exemplo.id)
    
    pedido_service.adicionar_item(
        pedido_id=pedido.id,
        produto_id=produto_exemplo.id,
        quantidade=2,  # Quantidade abaixo do mínimo
        comprador="Maria"
    )
    
    pedido_service.fechar_pedido(pedido.id)
    pedido_processado = pedido_service.processar_pedido(pedido.id)
    
    assert pedido_processado.status == "processado"
    assert pedido_processado.itens[0].quantidade_ajustada >= produto_exemplo.quantidade_minima_por_pedido

def test_remover_item_pedido(pedido_service, catalogo_exemplo, produto_exemplo):
    """Deve remover um item do pedido com sucesso."""
    pedido = pedido_service.criar_pedido(catalogo_exemplo.id)
    
    item = pedido_service.adicionar_item(
        pedido_id=pedido.id,
        produto_id=produto_exemplo.id,
        quantidade=5,
        comprador="Maria"
    )
    
    resultado = pedido_service.remover_item(pedido.id, item.id)
    
    assert resultado is True
    pedido_atualizado = pedido_service.buscar_pedido(pedido.id)
    assert len(pedido_atualizado.itens) == 0

def test_listar_pedidos_por_catalogo(pedido_service, catalogo_exemplo):
    """Deve listar pedidos de um catálogo com sucesso."""
    # Cria dois pedidos para o mesmo catálogo
    pedido_service.criar_pedido(catalogo_exemplo.id)
    pedido_service.criar_pedido(catalogo_exemplo.id)
    
    pedidos = pedido_service.listar_pedidos_por_catalogo(catalogo_exemplo.id)
    
    assert len(pedidos) == 2
    assert all(p.catalogo_id == catalogo_exemplo.id for p in pedidos)

def test_erro_pedido_fechado(pedido_service, catalogo_exemplo, produto_exemplo):
    """Deve lançar erro ao tentar modificar pedido fechado."""
    pedido = pedido_service.criar_pedido(catalogo_exemplo.id)
    pedido_service.fechar_pedido(pedido.id)
    
    with pytest.raises(ValueError):
        pedido_service.adicionar_item(
            pedido_id=pedido.id,
            produto_id=produto_exemplo.id,
            quantidade=5,
            comprador="Maria"
        ) 