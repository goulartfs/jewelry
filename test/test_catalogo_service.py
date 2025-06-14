"""
Testes para o serviço de Catálogo.
"""
import pytest
from datetime import datetime, timedelta
from domain.catalogo.models import Catalogo, Produto
from domain.catalogo.service import CatalogoService

@pytest.fixture
def catalogo_service():
    return CatalogoService()

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

def test_criar_catalogo(catalogo_service):
    """Deve criar um catálogo com sucesso."""
    data_inicio = datetime.now()
    data_fim = data_inicio + timedelta(days=30)
    
    catalogo = catalogo_service.criar_catalogo(
        nome="Catálogo Primavera",
        fornecedor="Joias & Cia",
        data_inicio=data_inicio,
        data_fim=data_fim
    )
    
    assert catalogo is not None
    assert catalogo.nome == "Catálogo Primavera"
    assert catalogo.fornecedor == "Joias & Cia"
    assert catalogo.data_inicio == data_inicio
    assert catalogo.data_fim == data_fim
    assert catalogo.ativo is True
    assert len(catalogo.produtos) == 0

def test_adicionar_produto(catalogo_service, produto_exemplo):
    """Deve adicionar um produto ao catálogo com sucesso."""
    catalogo = catalogo_service.criar_catalogo(
        nome="Catálogo Verão",
        fornecedor="Joias & Cia",
        data_inicio=datetime.now(),
        data_fim=datetime.now() + timedelta(days=30)
    )
    
    resultado = catalogo_service.adicionar_produto(
        catalogo_id=catalogo.id,
        produto=produto_exemplo
    )
    
    assert resultado is True
    catalogo_atualizado = catalogo_service.buscar_catalogo(catalogo.id)
    assert len(catalogo_atualizado.produtos) == 1
    assert catalogo_atualizado.produtos[0].nome == "Anel Esmeralda"

def test_listar_catalogos_ativos(catalogo_service):
    """Deve listar apenas catálogos ativos."""
    # Cria um catálogo ativo
    catalogo_service.criar_catalogo(
        nome="Catálogo Ativo",
        fornecedor="Joias & Cia",
        data_inicio=datetime.now(),
        data_fim=datetime.now() + timedelta(days=30)
    )
    
    # Cria um catálogo inativo (data_fim no passado)
    catalogo_service.criar_catalogo(
        nome="Catálogo Inativo",
        fornecedor="Joias & Cia",
        data_inicio=datetime.now() - timedelta(days=60),
        data_fim=datetime.now() - timedelta(days=30)
    )
    
    catalogos_ativos = catalogo_service.listar_catalogos_ativos()
    
    assert len(catalogos_ativos) == 1
    assert catalogos_ativos[0].nome == "Catálogo Ativo"

def test_remover_produto(catalogo_service, produto_exemplo):
    """Deve remover um produto do catálogo com sucesso."""
    catalogo = catalogo_service.criar_catalogo(
        nome="Catálogo Teste",
        fornecedor="Joias & Cia",
        data_inicio=datetime.now(),
        data_fim=datetime.now() + timedelta(days=30)
    )
    
    catalogo_service.adicionar_produto(catalogo.id, produto_exemplo)
    resultado = catalogo_service.remover_produto(catalogo.id, produto_exemplo.id)
    
    assert resultado is True
    catalogo_atualizado = catalogo_service.buscar_catalogo(catalogo.id)
    assert len(catalogo_atualizado.produtos) == 0

def test_buscar_catalogo_inexistente(catalogo_service):
    """Deve retornar None ao buscar catálogo inexistente."""
    catalogo = catalogo_service.buscar_catalogo(999)
    assert catalogo is None 