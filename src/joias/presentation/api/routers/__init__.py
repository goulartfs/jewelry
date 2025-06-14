"""
Pacote de routers da API.

Este pacote contém todos os routers da API FastAPI,
organizados por domínio.
"""
from .auth import router as auth_router
from .orders import router as orders_router
from .products import router as products_router
from .suppliers import router as suppliers_router
from .users import router as users_router

__all__ = [
    "auth_router",
    "users_router",
    "products_router",
    "orders_router",
    "suppliers_router",
]
