"""
Testes de integração para as rotas de usuário.

Este módulo contém os testes que validam o comportamento
das rotas de usuário da API.
"""
import pytest
from fastapi.testclient import TestClient

from src.joias.presentation.api.main import app


@pytest.fixture
def client():
    """Fixture que retorna um cliente de teste da API."""
    return TestClient(app)


def test_criar_usuario(client):
    """Deve criar um usuário via API."""
    # Arrange
    dados = {"nome": "João da Silva", "email": "joao@email.com", "senha": "senha123"}

    # Act
    response = client.post("/api/usuarios", json=dados)

    # Assert
    assert response.status_code == 201
    assert response.json()["nome"] == dados["nome"]
    assert response.json()["email"] == dados["email"]
    assert "senha" not in response.json()
    assert response.json()["ativo"] is True


def test_criar_usuario_dados_invalidos(client):
    """Deve retornar erro ao criar usuário com dados inválidos."""
    # Arrange
    dados = {
        "nome": "",  # Nome vazio
        "email": "email_invalido",  # Email inválido
        "senha": "123",  # Senha muito curta
    }

    # Act
    response = client.post("/api/usuarios", json=dados)

    # Assert
    assert response.status_code == 400
    assert "erro" in response.json()


def test_criar_usuario_email_duplicado(client):
    """Deve retornar erro ao criar usuário com email duplicado."""
    # Arrange
    dados = {"nome": "João da Silva", "email": "joao@email.com", "senha": "senha123"}
    client.post("/api/usuarios", json=dados)

    # Act
    response = client.post("/api/usuarios", json=dados)

    # Assert
    assert response.status_code == 409
    assert "já cadastrado" in response.json()["erro"].lower()


def test_buscar_usuario(client):
    """Deve buscar um usuário pelo ID."""
    # Arrange
    dados = {"nome": "João da Silva", "email": "joao@email.com", "senha": "senha123"}
    criado = client.post("/api/usuarios", json=dados).json()

    # Act
    response = client.get(f"/api/usuarios/{criado['id']}")

    # Assert
    assert response.status_code == 200
    assert response.json()["id"] == criado["id"]
    assert response.json()["nome"] == dados["nome"]
    assert response.json()["email"] == dados["email"]


def test_buscar_usuario_inexistente(client):
    """Deve retornar erro ao buscar usuário inexistente."""
    # Act
    response = client.get("/api/usuarios/999")

    # Assert
    assert response.status_code == 404
    assert "não encontrado" in response.json()["erro"].lower()


def test_listar_usuarios(client):
    """Deve listar usuários com paginação."""
    # Arrange
    for i in range(5):
        dados = {
            "nome": f"Usuário {i}",
            "email": f"usuario{i}@email.com",
            "senha": "senha123",
        }
        client.post("/api/usuarios", json=dados)

    # Act
    response = client.get("/api/usuarios")

    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 5


def test_listar_usuarios_paginacao(client):
    """Deve paginar a listagem de usuários."""
    # Arrange
    for i in range(15):
        dados = {
            "nome": f"Usuário {i}",
            "email": f"usuario{i}@email.com",
            "senha": "senha123",
        }
        client.post("/api/usuarios", json=dados)

    # Act
    pagina1 = client.get("/api/usuarios?pagina=1&tamanho=10")
    pagina2 = client.get("/api/usuarios?pagina=2&tamanho=10")

    # Assert
    assert pagina1.status_code == 200
    assert pagina2.status_code == 200
    assert len(pagina1.json()) == 10
    assert len(pagina2.json()) == 5


def test_listar_usuarios_filtro_nome(client):
    """Deve filtrar usuários por nome."""
    # Arrange
    dados = {"nome": "João da Silva", "email": "joao@email.com", "senha": "senha123"}
    client.post("/api/usuarios", json=dados)

    # Act
    response = client.get("/api/usuarios?nome=João")

    # Assert
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["nome"] == dados["nome"]


def test_listar_usuarios_filtro_email(client):
    """Deve filtrar usuários por email."""
    # Arrange
    dados = {"nome": "João da Silva", "email": "joao@email.com", "senha": "senha123"}
    client.post("/api/usuarios", json=dados)

    # Act
    response = client.get("/api/usuarios?email=joao@email.com")

    # Assert
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["email"] == dados["email"]
