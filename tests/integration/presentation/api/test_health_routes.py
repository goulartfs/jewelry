"""
Testes de integração para os endpoints de health check.
"""
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_health_check():
    """Testa o endpoint de health check."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_db_health_check(client):
    """
    Testa o endpoint de health check do banco de dados.
    
    Args:
        client: Cliente de teste
    """
    response = client.get("/api/v1/health/db")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"} 