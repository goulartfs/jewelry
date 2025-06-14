"""
Serviço de autenticação.

Este módulo implementa o serviço de autenticação da aplicação,
incluindo geração e validação de tokens JWT.
"""
import os
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ...domain.identity.entities.usuario import Usuario
from ...domain.shared.value_objects.email import Email
from ...infrastructure.persistence.sqlalchemy.repositories.usuario_repository import (
    UsuarioRepository,
)


class AuthService:
    """
    Serviço de autenticação.

    Esta classe implementa a lógica de autenticação, incluindo:
    - Autenticação de usuários
    - Geração de tokens JWT
    - Validação de tokens
    - Gerenciamento de senhas
    """

    def __init__(self, db: Session):
        """
        Inicializa o serviço de autenticação.

        Args:
            db: Sessão do banco de dados
        """
        self.db = db
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = os.getenv("SECRET_KEY", "your-secret-key")
        self.algorithm = "HS256"
        self.usuario_repository = UsuarioRepository(db)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verifica se uma senha está correta.

        Args:
            plain_password: Senha em texto plano
            hashed_password: Hash da senha

        Returns:
            bool: True se a senha estiver correta
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """
        Gera o hash de uma senha.

        Args:
            password: Senha em texto plano

        Returns:
            str: Hash da senha
        """
        return self.pwd_context.hash(password)

    def authenticate(self, email: Email, password: str) -> Optional[Usuario]:
        """
        Autentica um usuário.

        Args:
            email: Email do usuário
            password: Senha em texto plano

        Returns:
            Optional[Usuario]: Usuário autenticado ou None
        """
        user = self.usuario_repository.buscar_por_email(email)
        if not user:
            return None
        if not self.verify_password(password, user.senha_hash):
            return None
        return user

    def create_access_token(
        self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Cria um token de acesso JWT.

        Args:
            data: Dados a serem incluídos no token
            expires_delta: Tempo de expiração do token

        Returns:
            str: Token JWT
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def get_user(self, user_id: str) -> Optional[Usuario]:
        """
        Busca um usuário pelo ID.

        Args:
            user_id: ID do usuário

        Returns:
            Optional[Usuario]: Usuário encontrado ou None
        """
        return self.usuario_repository.buscar_por_id(user_id)
