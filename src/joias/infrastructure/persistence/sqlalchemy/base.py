"""
Classe base para modelos SQLAlchemy.

Este módulo define a classe base para todos os modelos
SQLAlchemy da aplicação.
"""
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
