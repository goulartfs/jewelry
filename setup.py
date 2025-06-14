"""
Configuração do projeto joias.

Este arquivo contém as configurações necessárias para instalar
e distribuir o pacote joias.
"""
from setuptools import setup, find_packages

setup(
    name="joias",
    version="0.1.0",
    description="Sistema de gestão de joias",
    author="FSynthis",
    author_email="fsynthis@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi>=0.68.0",
        "sqlalchemy>=1.4.0",
        "pydantic>=1.8.0",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        "python-multipart>=0.0.5",
        "uvicorn>=0.15.0",
        "alembic>=1.7.0",
        "psycopg2-binary>=2.9.0",
        "pytest>=6.2.0",
        "pytest-cov>=2.12.0",
        "pytest-asyncio>=0.15.0",
        "httpx>=0.18.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
) 