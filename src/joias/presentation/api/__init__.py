"""
Pacote da API REST.

Este pacote contém a implementação da API REST usando FastAPI,
incluindo rotas, schemas e dependências.
"""
from .main import app
from .routers import (
    auth_router,
    users_router,
    products_router,
    orders_router,
    suppliers_router
)
from .schemas import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserList
)
from .dependencies import (
    get_current_user,
    get_current_active_user
)

__all__ = [
    'app',
    'auth_router',
    'users_router',
    'products_router',
    'orders_router',
    'suppliers_router',
    'UserBase',
    'UserCreate',
    'UserUpdate',
    'UserResponse',
    'UserList',
    'get_current_user',
    'get_current_active_user'
] 