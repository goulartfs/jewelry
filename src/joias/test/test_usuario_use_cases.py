"""
Testes para os casos de uso de usuários.

Este módulo contém os testes unitários para os casos de uso
relacionados a usuários.
"""
import pytest
from datetime import datetime

from ..domain.entities.usuario import Usuario
from ..domain.entities.autorizacao import Perfil, Permissao
from ..domain.entities.dados_pessoais import DadoPessoal
from ..domain.entities.empresa import Empresa
from ..application.use_cases.usuario import (
    CriarUsuarioInput,
    CriarUsuarioUseCase,
    AtualizarUsuarioInput,
    AtualizarUsuarioUseCase,
    DeletarUsuarioUseCase,
    ListarUsuariosEmpresaUseCase
)
from ..infrastructure.repositories.memory.usuario import MemoryUsuarioRepository


@pytest.fixture
def usuario_repository():
    """Fixture que cria um repositório de usuários em memória."""
    return MemoryUsuarioRepository()


@pytest.fixture
def perfil():
    """Fixture que cria um perfil de usuário."""
    permissoes = [
        Permissao(nome="Criar Pedido", descricao="Pode criar pedidos", codigo="CRIAR_PEDIDO"),
        Permissao(nome="Listar Pedidos", descricao="Pode listar pedidos", codigo="LISTAR_PEDIDOS")
    ]
    return Perfil(nome="Cliente", descricao="Perfil de cliente", permissoes=permissoes)


@pytest.fixture
def dados_pessoais():
    """Fixture que cria dados pessoais."""
    return DadoPessoal(
        nome="João Silva",
        cpf="123.456.789-00",
        data_nascimento=datetime(1990, 1, 1)
    )


@pytest.fixture
def empresa():
    """Fixture que cria uma empresa."""
    return Empresa(
        razao_social="Empresa Teste LTDA",
        nome_fantasia="Empresa Teste",
        cnpj="12.345.678/0001-90",
        endereco=None  # TODO: Adicionar endereço
    )


def test_criar_usuario(usuario_repository, perfil, dados_pessoais):
    """Testa a criação de um usuário."""
    use_case = CriarUsuarioUseCase(usuario_repository)
    input_data = CriarUsuarioInput(
        username="joao.silva",
        email="joao.silva@example.com",
        senha="senha123",
        perfil=perfil,
        dados_pessoais=dados_pessoais
    )

    usuario = use_case.execute(input_data)

    assert usuario.id is not None
    assert usuario.username == "joao.silva"
    assert usuario.email == "joao.silva@example.com"
    assert usuario.perfil == perfil
    assert usuario.dados_pessoais == dados_pessoais


def test_criar_usuario_username_duplicado(usuario_repository, perfil, dados_pessoais):
    """Testa a tentativa de criar um usuário com username duplicado."""
    use_case = CriarUsuarioUseCase(usuario_repository)
    input_data = CriarUsuarioInput(
        username="joao.silva",
        email="joao.silva@example.com",
        senha="senha123",
        perfil=perfil,
        dados_pessoais=dados_pessoais
    )

    use_case.execute(input_data)

    with pytest.raises(ValueError, match="Username já existe"):
        use_case.execute(input_data)


def test_atualizar_usuario(usuario_repository, perfil, dados_pessoais):
    """Testa a atualização de um usuário."""
    # Cria um usuário
    criar_use_case = CriarUsuarioUseCase(usuario_repository)
    usuario = criar_use_case.execute(CriarUsuarioInput(
        username="joao.silva",
        email="joao.silva@example.com",
        senha="senha123",
        perfil=perfil,
        dados_pessoais=dados_pessoais
    ))

    # Atualiza o usuário
    atualizar_use_case = AtualizarUsuarioUseCase(usuario_repository)
    novo_email = "joao.silva.novo@example.com"
    usuario_atualizado = atualizar_use_case.execute(AtualizarUsuarioInput(
        id=usuario.id,
        email=novo_email
    ))

    assert usuario_atualizado.email == novo_email


def test_deletar_usuario(usuario_repository, perfil, dados_pessoais):
    """Testa a deleção de um usuário."""
    # Cria um usuário
    criar_use_case = CriarUsuarioUseCase(usuario_repository)
    usuario = criar_use_case.execute(CriarUsuarioInput(
        username="joao.silva",
        email="joao.silva@example.com",
        senha="senha123",
        perfil=perfil,
        dados_pessoais=dados_pessoais
    ))

    # Deleta o usuário
    deletar_use_case = DeletarUsuarioUseCase(usuario_repository)
    deletar_use_case.execute(usuario.id)

    # Verifica se o usuário foi deletado
    assert usuario_repository.buscar_por_id(usuario.id) is None


def test_listar_usuarios_empresa(usuario_repository, perfil, dados_pessoais, empresa):
    """Testa a listagem de usuários de uma empresa."""
    # Cria alguns usuários
    criar_use_case = CriarUsuarioUseCase(usuario_repository)
    
    # Usuário 1 - Com empresa
    criar_use_case.execute(CriarUsuarioInput(
        username="usuario1",
        email="usuario1@example.com",
        senha="senha123",
        perfil=perfil,
        dados_pessoais=dados_pessoais,
        empresa=empresa
    ))

    # Usuário 2 - Com empresa
    criar_use_case.execute(CriarUsuarioInput(
        username="usuario2",
        email="usuario2@example.com",
        senha="senha123",
        perfil=perfil,
        dados_pessoais=dados_pessoais,
        empresa=empresa
    ))

    # Usuário 3 - Sem empresa
    criar_use_case.execute(CriarUsuarioInput(
        username="usuario3",
        email="usuario3@example.com",
        senha="senha123",
        perfil=perfil,
        dados_pessoais=dados_pessoais
    ))

    # Lista os usuários da empresa
    listar_use_case = ListarUsuariosEmpresaUseCase(usuario_repository)
    usuarios = listar_use_case.execute(empresa.id)

    assert len(usuarios) == 2
    assert all(u.empresa and u.empresa.id == empresa.id for u in usuarios) 