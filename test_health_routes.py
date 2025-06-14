"""
Testes para os endpoints de health check.
"""
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_check():
    """Testa o endpoint de health check."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"} 