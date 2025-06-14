"""
Pacote de objetos de valor compartilhados.

Este pacote contém as classes base e implementações comuns
de objetos de valor.
"""
from .value_object import ValueObject
from .email import Email

__all__ = ["ValueObject", "Email"]
