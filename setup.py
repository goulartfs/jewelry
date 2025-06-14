"""
Configuração do pacote.
"""
from setuptools import setup, find_packages

setup(
    name="joias",
    version="0.1.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi==0.109.2",
        "uvicorn==0.27.1",
        "sqlalchemy==2.0.27",
        "psycopg2-binary==2.9.9",
        "pydantic==2.6.1",
        "pydantic-settings==2.1.0",
        "python-jose==3.3.0",
        "passlib==1.7.4",
        "python-multipart==0.0.9",
        "python-dotenv==1.0.1",
        "bcrypt==4.1.2",
    ],
    extras_require={
        "test": [
            "pytest==8.0.2",
            "httpx==0.27.0",
        ],
    },
) 