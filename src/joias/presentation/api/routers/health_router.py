"""
Router para health check.

Este módulo define os endpoints para verificar a saúde da aplicação.
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Verifica se a aplicação está funcionando.
    
    Returns:
        dict: Status da aplicação
    """
    return {"status": "ok"} 