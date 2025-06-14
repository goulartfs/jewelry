"""
Pacote da API REST.

Este pacote contém a implementação da API REST usando FastAPI,
incluindo rotas, schemas e dependências.
"""
from .dependencies import get_current_active_user, get_current_user
from .main import app
from .routers import (
    auth_router,
    orders_router,
    products_router,
    suppliers_router,
    users_router,
)
from .schemas import UserBase, UserCreate, UserList, UserResponse, UserUpdate

__all__ = [
    "app",
    "auth_router",
    "users_router",
    "products_router",
    "orders_router",
    "suppliers_router",
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserList",
    "get_current_user",
    "get_current_active_user",
]
