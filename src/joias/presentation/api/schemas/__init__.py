"""
Pacote de schemas da API.

Este pacote contém todos os schemas Pydantic da API,
organizados por domínio.
"""
from .user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserList
)

__all__ = [
    'UserBase',
    'UserCreate',
    'UserUpdate',
    'UserResponse',
    'UserList'
] 