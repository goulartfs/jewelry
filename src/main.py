"""
Ponto de entrada da aplicação.

Este módulo inicializa a aplicação FastAPI.
"""
from fastapi import FastAPI

app = FastAPI(
    title="API de Joias",
    description="API para gerenciamento de joias",
    version="0.1.0",
)


@app.get("/api/v1/health")
async def health_check():
    """
    Verifica se a aplicação está funcionando.
    
    Returns:
        dict: Status da aplicação
    """
    return {"status": "ok"} 