"""
Testes para os casos de uso de produtos.

Este módulo contém os testes unitários para os casos de uso
relacionados a produtos.
"""
import pytest
from decimal import Decimal

from ..domain.entities.produto import Produto, Variacao, Detalhe
from ..application.use_cases.produto import (
    CriarProdutoInput,
    CriarProdutoUseCase,
    AtualizarProdutoInput,
    AtualizarProdutoUseCase,
    DeletarProdutoUseCase,
    AdicionarVariacaoInput,
    AdicionarVariacaoUseCase,
    AdicionarDetalheInput,
    AdicionarDetalheUseCase,
    BuscarProdutosUseCase
)
from ..infrastructure.repositories.memory.produto import (
    MemoryProdutoRepository,
    MemoryVariacaoRepository,
    MemoryDetalheRepository
)


@pytest.fixture
def produto_repository():
    """Fixture que cria um repositório de produtos em memória."""
    return MemoryProdutoRepository()


@pytest.fixture
def variacao_repository():
    """Fixture que cria um repositório de variações em memória."""
    return MemoryVariacaoRepository()


@pytest.fixture
def detalhe_repository():
    """Fixture que cria um repositório de detalhes em memória."""
    return MemoryDetalheRepository()


@pytest.fixture
def detalhe():
    """Fixture que cria um detalhe."""
    return Detalhe(
        nome="Material",
        valor="Ouro 18k",
        tipo="material"
    )


@pytest.fixture
def variacao():
    """Fixture que cria uma variação."""
    return Variacao(
        nome="Aro 18",
        descricao="Anel tamanho aro 18",
        codigo="ANL-18"
    )


def test_criar_produto(produto_repository):
    """Testa a criação de um produto."""
    use_case = CriarProdutoUseCase(produto_repository)
    input_data = CriarProdutoInput(
        nome="Anel Solitário",
        descricao="Anel solitário em ouro 18k",
        codigo="ANL-001",
        preco=Decimal("1000.00")
    )

    produto = use_case.execute(input_data)

    assert produto.id is not None
    assert produto.nome == "Anel Solitário"
    assert produto.codigo == "ANL-001"
    assert produto.preco.valor == Decimal("1000.00")


def test_criar_produto_codigo_duplicado(produto_repository):
    """Testa a tentativa de criar um produto com código duplicado."""
    use_case = CriarProdutoUseCase(produto_repository)
    input_data = CriarProdutoInput(
        nome="Anel Solitário",
        descricao="Anel solitário em ouro 18k",
        codigo="ANL-001",
        preco=Decimal("1000.00")
    )

    use_case.execute(input_data)

    with pytest.raises(ValueError, match="Código já existe"):
        use_case.execute(input_data)


def test_atualizar_produto(produto_repository):
    """Testa a atualização de um produto."""
    # Cria um produto
    criar_use_case = CriarProdutoUseCase(produto_repository)
    produto = criar_use_case.execute(CriarProdutoInput(
        nome="Anel Solitário",
        descricao="Anel solitário em ouro 18k",
        codigo="ANL-001",
        preco=Decimal("1000.00")
    ))

    # Atualiza o produto
    atualizar_use_case = AtualizarProdutoUseCase(produto_repository)
    novo_preco = Decimal("1200.00")
    produto_atualizado = atualizar_use_case.execute(AtualizarProdutoInput(
        id=produto.id,
        preco=novo_preco
    ))

    assert produto_atualizado.preco.valor == novo_preco


def test_deletar_produto(produto_repository):
    """Testa a deleção de um produto."""
    # Cria um produto
    criar_use_case = CriarProdutoUseCase(produto_repository)
    produto = criar_use_case.execute(CriarProdutoInput(
        nome="Anel Solitário",
        descricao="Anel solitário em ouro 18k",
        codigo="ANL-001",
        preco=Decimal("1000.00")
    ))

    # Deleta o produto
    deletar_use_case = DeletarProdutoUseCase(produto_repository)
    deletar_use_case.execute(produto.id)

    # Verifica se o produto foi deletado
    assert produto_repository.buscar_por_id(produto.id) is None


def test_adicionar_variacao(produto_repository, variacao_repository):
    """Testa a adição de uma variação a um produto."""
    # Cria um produto
    criar_use_case = CriarProdutoUseCase(produto_repository)
    produto = criar_use_case.execute(CriarProdutoInput(
        nome="Anel Solitário",
        descricao="Anel solitário em ouro 18k",
        codigo="ANL-001",
        preco=Decimal("1000.00")
    ))

    # Adiciona uma variação
    adicionar_use_case = AdicionarVariacaoUseCase(
        produto_repository,
        variacao_repository
    )
    produto_atualizado = adicionar_use_case.execute(AdicionarVariacaoInput(
        produto_id=produto.id,
        nome="Aro 18",
        descricao="Anel tamanho aro 18",
        codigo="ANL-001-18"
    ))

    assert len(produto_atualizado.variacoes) == 1
    assert produto_atualizado.variacoes[0].nome == "Aro 18"


def test_adicionar_detalhe(produto_repository):
    """Testa a adição de um detalhe a um produto."""
    # Cria um produto
    criar_use_case = CriarProdutoUseCase(produto_repository)
    produto = criar_use_case.execute(CriarProdutoInput(
        nome="Anel Solitário",
        descricao="Anel solitário em ouro 18k",
        codigo="ANL-001",
        preco=Decimal("1000.00")
    ))

    # Adiciona um detalhe
    adicionar_use_case = AdicionarDetalheUseCase(produto_repository)
    produto_atualizado = adicionar_use_case.execute(AdicionarDetalheInput(
        produto_id=produto.id,
        nome="Material",
        valor="Ouro 18k",
        tipo="material"
    ))

    assert len(produto_atualizado.detalhes) == 1
    assert produto_atualizado.detalhes[0].nome == "Material"
    assert produto_atualizado.detalhes[0].valor == "Ouro 18k"


def test_buscar_produtos(produto_repository):
    """Testa a busca de produtos por nome."""
    # Cria alguns produtos
    criar_use_case = CriarProdutoUseCase(produto_repository)
    
    # Produto 1
    criar_use_case.execute(CriarProdutoInput(
        nome="Anel Solitário",
        descricao="Anel solitário em ouro 18k",
        codigo="ANL-001",
        preco=Decimal("1000.00")
    ))

    # Produto 2
    criar_use_case.execute(CriarProdutoInput(
        nome="Anel Aparador",
        descricao="Anel aparador em ouro 18k",
        codigo="ANL-002",
        preco=Decimal("800.00")
    ))

    # Produto 3
    criar_use_case.execute(CriarProdutoInput(
        nome="Colar Veneziano",
        descricao="Colar veneziano em ouro 18k",
        codigo="COL-001",
        preco=Decimal("1500.00")
    ))

    # Busca produtos
    buscar_use_case = BuscarProdutosUseCase(produto_repository)
    produtos = buscar_use_case.execute("Anel")

    assert len(produtos) == 2
    assert all("Anel" in p.nome for p in produtos) 