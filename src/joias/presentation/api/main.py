"""
Aplicação principal da API.

Este módulo configura e inicializa a aplicação FastAPI,
incluindo rotas, middlewares e dependências.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ...infrastructure.logging.config import setup_logging
from .routers import auth, orders, products, suppliers, users


def create_app() -> FastAPI:
    """
    Cria e configura a aplicação FastAPI.

    Returns:
        FastAPI: Aplicação configurada
    """
    # Configura o logging
    setup_logging()

    # Cria a aplicação
    app = FastAPI(
        title="Joias API",
        description="API para sistema de gestão de joias",
        version="0.1.0",
    )

    # Configura CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Em produção, especificar origens permitidas
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Inclui os routers
    app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
    app.include_router(users.router, prefix="/api/v1", tags=["users"])
    app.include_router(products.router, prefix="/api/v1", tags=["products"])
    app.include_router(orders.router, prefix="/api/v1", tags=["orders"])
    app.include_router(suppliers.router, prefix="/api/v1", tags=["suppliers"])

    return app


app = create_app()
