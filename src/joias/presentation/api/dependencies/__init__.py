"""
Pacote de dependências da API.

Este pacote contém todas as dependências do FastAPI,
incluindo autenticação, autorização e injeção de dependências.
"""
from .auth import get_current_user, get_current_active_user

__all__ = [
    'get_current_user',
    'get_current_active_user'
] 