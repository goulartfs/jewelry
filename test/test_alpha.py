"""
Testes para o módulo alpha.

Este módulo contém os testes unitários para as entidades e serviços do módulo alpha.
"""
import unittest
from datetime import datetime
from decimal import Decimal
from domain.alpha import (
    Usuario, Contato, DadoPessoal, Endereco, Empresa,
    Permissao, Perfil, Produto, Catalogo, Pedido, ItemPedido,
    Preco, Detalhe, Variacao,
    UsuarioService, ContatoService, DadoPessoalService,
    EmpresaService, PermissaoService, PerfilService,
    ProdutoService, CatalogoService, PedidoService
)

class TestBaseService(unittest.TestCase):
    """Testes para o serviço base."""

    def setUp(self):
        """Configura o ambiente de teste."""
        self.service = UsuarioService()  # Usando UsuarioService como exemplo
        self.perfil = Perfil(
            id=0,
            nome="Admin",
            descricao="Administrador do sistema",
            permissoes=[]
        )
        self.dados_pessoais = DadoPessoal(
            id=0,
            nome="John Doe",
            cpf="123.456.789-00",
            rg="12.345.678-9",
            data_nascimento=datetime(1990, 1, 1),
            enderecos=[]
        )
        self.usuario = Usuario(
            id=0,
            username="johndoe",
            email="john@example.com",
            senha_hash="hash123",
            perfil=self.perfil,
            dados_pessoais=self.dados_pessoais,
            empresa=None,
            data_ultimo_acesso=None
        )

    def test_create(self):
        """Testa a criação de um item."""
        usuario = self.service.create(self.usuario)
        self.assertEqual(usuario.id, 1)
        self.assertEqual(len(self.service.list()), 1)

    def test_get(self):
        """Testa a busca de um item."""
        usuario = self.service.create(self.usuario)
        found = self.service.get(usuario.id)
        self.assertEqual(found.username, "johndoe")

    def test_list(self):
        """Testa a listagem de itens."""
        self.service.create(self.usuario)
        items = self.service.list()
        self.assertEqual(len(items), 1)

    def test_update(self):
        """Testa a atualização de um item."""
        usuario = self.service.create(self.usuario)
        usuario.username = "janedoe"
        updated = self.service.update(usuario.id, usuario)
        self.assertEqual(updated.username, "janedoe")

    def test_delete(self):
        """Testa a remoção de um item."""
        usuario = self.service.create(self.usuario)
        self.assertTrue(self.service.delete(usuario.id))
        self.assertEqual(len(self.service.list()), 0)

    def test_soft_delete(self):
        """Testa a desativação de um item."""
        usuario = self.service.create(self.usuario)
        self.assertTrue(self.service.soft_delete(usuario.id))
        self.assertEqual(len(self.service.list()), 0)
        self.assertEqual(len(self.service.list(active_only=False)), 1)


class TestUsuarioService(unittest.TestCase):
    """Testes para o serviço de usuários."""

    def setUp(self):
        """Configura o ambiente de teste."""
        self.service = UsuarioService()
        self.perfil = Perfil(
            id=0,
            nome="Admin",
            descricao="Administrador do sistema",
            permissoes=[]
        )
        self.dados_pessoais = DadoPessoal(
            id=0,
            nome="John Doe",
            cpf="123.456.789-00",
            rg="12.345.678-9",
            data_nascimento=datetime(1990, 1, 1),
            enderecos=[]
        )
        self.usuario = Usuario(
            id=0,
            username="johndoe",
            email="john@example.com",
            senha_hash="hash123",
            perfil=self.perfil,
            dados_pessoais=self.dados_pessoais,
            empresa=None,
            data_ultimo_acesso=None
        )

    def test_get_by_email(self):
        """Testa a busca de usuário por email."""
        self.service.create(self.usuario)
        found = self.service.get_by_email("john@example.com")
        self.assertEqual(found.username, "johndoe")

    def test_get_by_username(self):
        """Testa a busca de usuário por username."""
        self.service.create(self.usuario)
        found = self.service.get_by_username("johndoe")
        self.assertEqual(found.email, "john@example.com")

    def test_update_last_access(self):
        """Testa a atualização da data de último acesso."""
        usuario = self.service.create(self.usuario)
        self.assertTrue(self.service.update_last_access(usuario.id))
        updated = self.service.get(usuario.id)
        self.assertIsNotNone(updated.data_ultimo_acesso)


class TestPedidoService(unittest.TestCase):
    """Testes para o serviço de pedidos."""

    def setUp(self):
        """Configura o ambiente de teste."""
        self.service = PedidoService()
        self.perfil = Perfil(
            id=0,
            nome="Cliente",
            descricao="Cliente do sistema",
            permissoes=[]
        )
        self.dados_pessoais = DadoPessoal(
            id=0,
            nome="John Doe",
            cpf="123.456.789-00",
            rg="12.345.678-9",
            data_nascimento=datetime(1990, 1, 1),
            enderecos=[]
        )
        self.usuario = Usuario(
            id=0,
            username="johndoe",
            email="john@example.com",
            senha_hash="hash123",
            perfil=self.perfil,
            dados_pessoais=self.dados_pessoais,
            empresa=None,
            data_ultimo_acesso=None
        )
        self.preco = Preco(
            id=0,
            valor=Decimal("100.00")
        )
        self.produto = Produto(
            id=0,
            nome="Anel de Ouro",
            descricao="Anel de ouro 18k",
            codigo="ANL-001",
            preco=self.preco,
            variacoes=[],
            detalhes=[]
        )
        self.item_pedido = ItemPedido(
            id=0,
            produto=self.produto,
            quantidade=1,
            preco_unitario=Decimal("100.00")
        )
        self.pedido = Pedido(
            id=0,
            usuario=self.usuario,
            itens=[]
        )

    def test_get_by_usuario(self):
        """Testa a busca de pedidos por usuário."""
        pedido = self.service.create(self.pedido)
        found = self.service.get_by_usuario(self.usuario.id)
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].id, pedido.id)

    def test_add_item(self):
        """Testa a adição de item ao pedido."""
        pedido = self.service.create(self.pedido)
        self.assertTrue(self.service.add_item(pedido.id, self.item_pedido))
        updated = self.service.get(pedido.id)
        self.assertEqual(len(updated.itens), 1)

    def test_confirmar_pedido(self):
        """Testa a confirmação de pedido."""
        pedido = self.service.create(self.pedido)
        self.service.add_item(pedido.id, self.item_pedido)
        self.assertTrue(self.service.confirmar_pedido(pedido.id))
        updated = self.service.get(pedido.id)
        self.assertEqual(updated.status, "confirmado")

    def test_cancelar_pedido(self):
        """Testa o cancelamento de pedido."""
        pedido = self.service.create(self.pedido)
        self.service.add_item(pedido.id, self.item_pedido)
        self.service.confirmar_pedido(pedido.id)
        self.assertTrue(self.service.cancelar_pedido(pedido.id))
        updated = self.service.get(pedido.id)
        self.assertEqual(updated.status, "cancelado")


class TestContatoService(unittest.TestCase):
    """Testes para o serviço de contatos."""

    def setUp(self):
        """Configura o ambiente de teste."""
        self.service = ContatoService()
        self.dados_pessoais = DadoPessoal(
            id=0,
            nome="John Doe",
            cpf="123.456.789-00",
            rg="12.345.678-9",
            data_nascimento=datetime(1990, 1, 1),
            enderecos=[]
        )
        self.contato = Contato(
            id=0,
            email="john@example.com",
            telefone="(11) 99999-9999",
            dados_pessoais=[self.dados_pessoais]
        )

    def test_create_contato(self):
        """Testa a criação de um contato."""
        contato = self.service.create(self.contato)
        self.assertEqual(contato.id, 1)
        self.assertEqual(contato.email, "john@example.com")
        self.assertEqual(len(contato.dados_pessoais), 1)

    def test_get_by_email(self):
        """Testa a busca de contato por email."""
        self.service.create(self.contato)
        found = self.service.get_by_email("john@example.com")
        self.assertIsNotNone(found)
        self.assertEqual(found.telefone, "(11) 99999-9999")

    def test_get_by_email_not_found(self):
        """Testa a busca de contato por email inexistente."""
        found = self.service.get_by_email("nonexistent@example.com")
        self.assertIsNone(found)

    def test_update_contato(self):
        """Testa a atualização de um contato."""
        contato = self.service.create(self.contato)
        contato.telefone = "(11) 88888-8888"
        updated = self.service.update(contato.id, contato)
        self.assertEqual(updated.telefone, "(11) 88888-8888")

    def test_soft_delete_contato(self):
        """Testa a desativação de um contato."""
        contato = self.service.create(self.contato)
        self.assertTrue(self.service.soft_delete(contato.id))
        self.assertEqual(len(self.service.list()), 0)
        self.assertEqual(len(self.service.list(active_only=False)), 1)


class TestDadoPessoalService(unittest.TestCase):
    """Testes para o serviço de dados pessoais."""

    def setUp(self):
        """Configura o ambiente de teste."""
        self.service = DadoPessoalService()
        self.endereco = Endereco(
            id=0,
            logradouro="Rua Teste",
            numero="123",
            complemento="Apto 456",
            bairro="Centro",
            cidade="São Paulo",
            estado="SP",
            cep="01234-567"
        )
        self.dados_pessoais = DadoPessoal(
            id=0,
            nome="John Doe",
            cpf="123.456.789-00",
            rg="12.345.678-9",
            data_nascimento=datetime(1990, 1, 1),
            enderecos=[self.endereco]
        )

    def test_create_dados_pessoais(self):
        """Testa a criação de dados pessoais."""
        dados = self.service.create(self.dados_pessoais)
        self.assertEqual(dados.id, 1)
        self.assertEqual(dados.nome, "John Doe")
        self.assertEqual(len(dados.enderecos), 1)

    def test_get_by_cpf(self):
        """Testa a busca de dados pessoais por CPF."""
        self.service.create(self.dados_pessoais)
        found = self.service.get_by_cpf("123.456.789-00")
        self.assertIsNotNone(found)
        self.assertEqual(found.nome, "John Doe")

    def test_get_by_cpf_not_found(self):
        """Testa a busca de dados pessoais por CPF inexistente."""
        found = self.service.get_by_cpf("999.999.999-99")
        self.assertIsNone(found)

    def test_update_dados_pessoais(self):
        """Testa a atualização de dados pessoais."""
        dados = self.service.create(self.dados_pessoais)
        dados.nome = "Jane Doe"
        updated = self.service.update(dados.id, dados)
        self.assertEqual(updated.nome, "Jane Doe")

    def test_soft_delete_dados_pessoais(self):
        """Testa a desativação de dados pessoais."""
        dados = self.service.create(self.dados_pessoais)
        self.assertTrue(self.service.soft_delete(dados.id))
        self.assertEqual(len(self.service.list()), 0)
        self.assertEqual(len(self.service.list(active_only=False)), 1)


class TestEmpresaService(unittest.TestCase):
    """Testes para o serviço de empresas."""

    def setUp(self):
        """Configura o ambiente de teste."""
        self.service = EmpresaService()
        self.endereco = Endereco(
            id=0,
            logradouro="Rua Comercial",
            numero="789",
            complemento="Sala 123",
            bairro="Centro",
            cidade="São Paulo",
            estado="SP",
            cep="04567-890"
        )
        self.dados_pessoais = DadoPessoal(
            id=0,
            nome="Responsável Legal",
            cpf="987.654.321-00",
            rg="98.765.432-1",
            data_nascimento=datetime(1980, 1, 1),
            enderecos=[]
        )
        self.contato = Contato(
            id=0,
            email="contato@empresa.com",
            telefone="(11) 3333-3333",
            dados_pessoais=[self.dados_pessoais]
        )
        self.empresa = Empresa(
            id=0,
            razao_social="Empresa Teste LTDA",
            nome_fantasia="Empresa Teste",
            cnpj="12.345.678/0001-90",
            inscricao_estadual="123456789",
            inscricao_municipal="987654321",
            endereco=self.endereco,
            contato=self.contato
        )

    def test_create_empresa(self):
        """Testa a criação de uma empresa."""
        empresa = self.service.create(self.empresa)
        self.assertEqual(empresa.id, 1)
        self.assertEqual(empresa.razao_social, "Empresa Teste LTDA")
        self.assertIsNotNone(empresa.endereco)
        self.assertIsNotNone(empresa.contato)

    def test_get_by_cnpj(self):
        """Testa a busca de empresa por CNPJ."""
        self.service.create(self.empresa)
        found = self.service.get_by_cnpj("12.345.678/0001-90")
        self.assertIsNotNone(found)
        self.assertEqual(found.nome_fantasia, "Empresa Teste")

    def test_get_by_cnpj_not_found(self):
        """Testa a busca de empresa por CNPJ inexistente."""
        found = self.service.get_by_cnpj("99.999.999/9999-99")
        self.assertIsNone(found)

    def test_update_empresa(self):
        """Testa a atualização de uma empresa."""
        empresa = self.service.create(self.empresa)
        empresa.nome_fantasia = "Novo Nome Fantasia"
        updated = self.service.update(empresa.id, empresa)
        self.assertEqual(updated.nome_fantasia, "Novo Nome Fantasia")

    def test_soft_delete_empresa(self):
        """Testa a desativação de uma empresa."""
        empresa = self.service.create(self.empresa)
        self.assertTrue(self.service.soft_delete(empresa.id))
        self.assertEqual(len(self.service.list()), 0)
        self.assertEqual(len(self.service.list(active_only=False)), 1)


class TestPermissaoService(unittest.TestCase):
    """Testes para o serviço de permissões."""

    def setUp(self):
        """Configura o ambiente de teste."""
        self.service = PermissaoService()
        self.permissao = Permissao(
            id=0,
            nome="Criar Pedido",
            descricao="Permite criar novos pedidos",
            codigo="CRIAR_PEDIDO"
        )

    def test_create_permissao(self):
        """Testa a criação de uma permissão."""
        permissao = self.service.create(self.permissao)
        self.assertEqual(permissao.id, 1)
        self.assertEqual(permissao.nome, "Criar Pedido")
        self.assertEqual(permissao.codigo, "CRIAR_PEDIDO")

    def test_get_by_codigo(self):
        """Testa a busca de permissão por código."""
        self.service.create(self.permissao)
        found = self.service.get_by_codigo("CRIAR_PEDIDO")
        self.assertIsNotNone(found)
        self.assertEqual(found.nome, "Criar Pedido")

    def test_get_by_codigo_not_found(self):
        """Testa a busca de permissão por código inexistente."""
        found = self.service.get_by_codigo("CODIGO_INEXISTENTE")
        self.assertIsNone(found)

    def test_update_permissao(self):
        """Testa a atualização de uma permissão."""
        permissao = self.service.create(self.permissao)
        permissao.descricao = "Nova descrição da permissão"
        updated = self.service.update(permissao.id, permissao)
        self.assertEqual(updated.descricao, "Nova descrição da permissão")

    def test_soft_delete_permissao(self):
        """Testa a desativação de uma permissão."""
        permissao = self.service.create(self.permissao)
        self.assertTrue(self.service.soft_delete(permissao.id))
        self.assertEqual(len(self.service.list()), 0)
        self.assertEqual(len(self.service.list(active_only=False)), 1)


class TestPerfilService(unittest.TestCase):
    """Testes para o serviço de perfis."""

    def setUp(self):
        """Configura o ambiente de teste."""
        self.service = PerfilService()
        self.permissao1 = Permissao(
            id=1,
            nome="Criar Pedido",
            descricao="Permite criar novos pedidos",
            codigo="CRIAR_PEDIDO"
        )
        self.permissao2 = Permissao(
            id=2,
            nome="Editar Pedido",
            descricao="Permite editar pedidos existentes",
            codigo="EDITAR_PEDIDO"
        )
        self.perfil = Perfil(
            id=0,
            nome="Vendedor",
            descricao="Perfil para vendedores",
            permissoes=[self.permissao1]
        )

    def test_create_perfil(self):
        """Testa a criação de um perfil."""
        perfil = self.service.create(self.perfil)
        self.assertEqual(perfil.id, 1)
        self.assertEqual(perfil.nome, "Vendedor")
        self.assertEqual(len(perfil.permissoes), 1)

    def test_add_permissao(self):
        """Testa a adição de uma permissão ao perfil."""
        perfil = self.service.create(self.perfil)
        self.assertTrue(self.service.add_permissao(perfil.id, self.permissao2))
        updated = self.service.get(perfil.id)
        self.assertEqual(len(updated.permissoes), 2)

    def test_add_permissao_duplicada(self):
        """Testa a adição de uma permissão duplicada ao perfil."""
        perfil = self.service.create(self.perfil)
        self.assertFalse(self.service.add_permissao(perfil.id, self.permissao1))
        updated = self.service.get(perfil.id)
        self.assertEqual(len(updated.permissoes), 1)

    def test_remove_permissao(self):
        """Testa a remoção de uma permissão do perfil."""
        perfil = self.service.create(self.perfil)
        self.assertTrue(self.service.remove_permissao(perfil.id, self.permissao1.id))
        updated = self.service.get(perfil.id)
        self.assertEqual(len(updated.permissoes), 0)

    def test_update_perfil(self):
        """Testa a atualização de um perfil."""
        perfil = self.service.create(self.perfil)
        perfil.descricao = "Nova descrição do perfil"
        updated = self.service.update(perfil.id, perfil)
        self.assertEqual(updated.descricao, "Nova descrição do perfil")

    def test_soft_delete_perfil(self):
        """Testa a desativação de um perfil."""
        perfil = self.service.create(self.perfil)
        self.assertTrue(self.service.soft_delete(perfil.id))
        self.assertEqual(len(self.service.list()), 0)
        self.assertEqual(len(self.service.list(active_only=False)), 1)


class TestCatalogoService(unittest.TestCase):
    """Testes para o serviço de catálogos."""

    def setUp(self):
        """Configura o ambiente de teste."""
        self.service = CatalogoService()
        self.perfil = Perfil(
            id=1,
            nome="Vendedor",
            descricao="Perfil para vendedores",
            permissoes=[]
        )
        self.dados_pessoais = DadoPessoal(
            id=1,
            nome="John Doe",
            cpf="123.456.789-00",
            rg="12.345.678-9",
            data_nascimento=datetime(1990, 1, 1),
            enderecos=[]
        )
        self.usuario = Usuario(
            id=1,
            username="johndoe",
            email="john@example.com",
            senha_hash="hash123",
            perfil=self.perfil,
            dados_pessoais=self.dados_pessoais,
            empresa=None,
            data_ultimo_acesso=None
        )
        self.preco = Preco(
            id=1,
            valor=Decimal("100.00")
        )
        self.produto = Produto(
            id=1,
            nome="Anel de Ouro",
            descricao="Anel de ouro 18k",
            codigo="ANL-001",
            preco=self.preco,
            variacoes=[],
            detalhes=[]
        )
        self.catalogo = Catalogo(
            id=0,
            nome="Catálogo de Joias",
            descricao="Catálogo principal de joias",
            usuario=self.usuario,
            produtos=[],
            data_inicio=datetime.now(),
            data_fim=datetime(2025, 12, 31)
        )

    def test_create_catalogo(self):
        """Testa a criação de um catálogo."""
        catalogo = self.service.create(self.catalogo)
        self.assertEqual(catalogo.id, 1)
        self.assertEqual(catalogo.nome, "Catálogo de Joias")
        self.assertEqual(len(catalogo.produtos), 0)

    def test_get_by_usuario(self):
        """Testa a busca de catálogos por usuário."""
        self.service.create(self.catalogo)
        found = self.service.get_by_usuario(self.usuario.id)
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].nome, "Catálogo de Joias")

    def test_add_produto(self):
        """Testa a adição de um produto ao catálogo."""
        catalogo = self.service.create(self.catalogo)
        self.assertTrue(self.service.add_produto(catalogo.id, self.produto))
        updated = self.service.get(catalogo.id)
        self.assertEqual(len(updated.produtos), 1)

    def test_add_produto_duplicado(self):
        """Testa a adição de um produto duplicado ao catálogo."""
        catalogo = self.service.create(self.catalogo)
        self.service.add_produto(catalogo.id, self.produto)
        self.assertFalse(self.service.add_produto(catalogo.id, self.produto))
        updated = self.service.get(catalogo.id)
        self.assertEqual(len(updated.produtos), 1)

    def test_update_catalogo(self):
        """Testa a atualização de um catálogo."""
        catalogo = self.service.create(self.catalogo)
        catalogo.descricao = "Nova descrição do catálogo"
        updated = self.service.update(catalogo.id, catalogo)
        self.assertEqual(updated.descricao, "Nova descrição do catálogo")

    def test_soft_delete_catalogo(self):
        """Testa a desativação de um catálogo."""
        catalogo = self.service.create(self.catalogo)
        self.assertTrue(self.service.soft_delete(catalogo.id))
        self.assertEqual(len(self.service.list()), 0)
        self.assertEqual(len(self.service.list(active_only=False)), 1)


class TestProdutoService(unittest.TestCase):
    """Testes para o serviço de produtos."""

    def setUp(self):
        """Configura o ambiente de teste."""
        self.service = ProdutoService()
        self.preco = Preco(
            id=0,
            valor=Decimal("100.00")
        )
        self.detalhe = Detalhe(
            id=0,
            nome="Material",
            valor="Ouro 18k",
            tipo="material"
        )
        self.variacao = Variacao(
            id=0,
            nome="Tamanho",
            descricao="Tamanho do anel",
            codigo="TAM-17",
            detalhes=[]
        )
        self.produto = Produto(
            id=0,
            nome="Anel de Ouro",
            descricao="Anel de ouro 18k",
            codigo="ANL-001",
            preco=self.preco,
            variacoes=[],
            detalhes=[]
        )

    def test_create_produto(self):
        """Testa a criação de um produto."""
        produto = self.service.create(self.produto)
        self.assertEqual(produto.id, 1)
        self.assertEqual(produto.nome, "Anel de Ouro")
        self.assertEqual(produto.codigo, "ANL-001")

    def test_get_by_codigo(self):
        """Testa a busca de produto por código."""
        self.service.create(self.produto)
        found = self.service.get_by_codigo("ANL-001")
        self.assertIsNotNone(found)
        self.assertEqual(found.nome, "Anel de Ouro")

    def test_get_by_codigo_not_found(self):
        """Testa a busca de produto por código inexistente."""
        found = self.service.get_by_codigo("CODIGO-INEXISTENTE")
        self.assertIsNone(found)

    def test_add_variacao(self):
        """Testa a adição de uma variação ao produto."""
        produto = self.service.create(self.produto)
        self.assertTrue(self.service.add_variacao(produto.id, self.variacao))
        updated = self.service.get(produto.id)
        self.assertEqual(len(updated.variacoes), 1)

    def test_add_variacao_duplicada(self):
        """Testa a adição de uma variação duplicada ao produto."""
        produto = self.service.create(self.produto)
        self.service.add_variacao(produto.id, self.variacao)
        self.assertFalse(self.service.add_variacao(produto.id, self.variacao))
        updated = self.service.get(produto.id)
        self.assertEqual(len(updated.variacoes), 1)

    def test_add_detalhe(self):
        """Testa a adição de um detalhe ao produto."""
        produto = self.service.create(self.produto)
        self.assertTrue(self.service.add_detalhe(produto.id, self.detalhe))
        updated = self.service.get(produto.id)
        self.assertEqual(len(updated.detalhes), 1)

    def test_add_detalhe_duplicado(self):
        """Testa a adição de um detalhe duplicado ao produto."""
        produto = self.service.create(self.produto)
        self.service.add_detalhe(produto.id, self.detalhe)
        self.assertFalse(self.service.add_detalhe(produto.id, self.detalhe))
        updated = self.service.get(produto.id)
        self.assertEqual(len(updated.detalhes), 1)

    def test_update_produto(self):
        """Testa a atualização de um produto."""
        produto = self.service.create(self.produto)
        produto.descricao = "Nova descrição do produto"
        updated = self.service.update(produto.id, produto)
        self.assertEqual(updated.descricao, "Nova descrição do produto")

    def test_soft_delete_produto(self):
        """Testa a desativação de um produto."""
        produto = self.service.create(self.produto)
        self.assertTrue(self.service.soft_delete(produto.id))
        self.assertEqual(len(self.service.list()), 0)
        self.assertEqual(len(self.service.list(active_only=False)), 1)


if __name__ == '__main__':
    unittest.main() 