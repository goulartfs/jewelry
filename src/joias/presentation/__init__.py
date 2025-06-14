"""
Pacote de apresentação.

Este pacote contém a camada de apresentação do sistema,
incluindo APIs REST, CLI e outras interfaces com o usuário.
"""
from .api.main import app

__all__ = ["app"]
