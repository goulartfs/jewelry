"""
Pacote de testes do sistema de joias.

Este pacote contém todos os testes do sistema, organizados por módulo
e tipo de teste (unitário, integração, etc.).
"""

import os
import sys

# Adiciona o diretório src ao PYTHONPATH para permitir importações relativas
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Configura variáveis de ambiente para testes
os.environ.setdefault('ENVIRONMENT', 'test')
os.environ.setdefault('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/joias_test') 