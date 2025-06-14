"""
Pacote de routers da API.

Este pacote contém todos os routers da API FastAPI,
organizados por domínio.
"""
from .auth import router as auth_router
from .orders import router as orders_router
from .perfil_router import router as perfil_router
from .products import router as products_router
from .suppliers import router as suppliers_router
from .users import router as users_router
from fastapi import APIRouter

from .permissao_router import router as permissao_router
from .usuario_router import router as usuario_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(permissao_router)
api_router.include_router(usuario_router)

__all__ = [
    "auth_router",
    "users_router",
    "products_router",
    "orders_router",
    "suppliers_router",
    "perfil_router",
]
