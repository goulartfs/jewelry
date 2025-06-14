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
from ...domain.repositories.usuario_repository import IUsuarioRepository
from ..shared.exceptions import AutenticacaoError, ValidacaoError

import bcrypt
from jwt.exceptions import InvalidTokenError


class AuthService:
    """
    Serviço para autenticação de usuários.
    """

    def __init__(
        self,
        usuario_repository: IUsuarioRepository,
        secret_key: str,
        token_expiration: int = 24,
    ):
        """
        Inicializa o serviço de autenticação.

        Args:
            usuario_repository: Repositório de usuários
            secret_key: Chave secreta para geração de tokens
            token_expiration: Tempo de expiração do token em horas (padrão: 24)
        """
        self._usuario_repository = usuario_repository
        self._secret_key = secret_key
        self._token_expiration = token_expiration

    def autenticar(self, email: str, senha: str) -> str:
        """
        Autentica um usuário.

        Args:
            email: Email do usuário
            senha: Senha do usuário

        Returns:
            Token JWT

        Raises:
            AutenticacaoError: Se as credenciais forem inválidas
            ValidacaoError: Se o email for inválido
        """
        try:
            email_obj = Email(email)
        except ValueError as e:
            raise ValidacaoError(str(e))

        usuario = self._usuario_repository.buscar_por_email(email_obj)
        if not usuario:
            raise AutenticacaoError("Credenciais inválidas")

        if not usuario.ativo:
            raise AutenticacaoError("Usuário inativo")

        if not self._verificar_senha(senha, usuario.senha_hash):
            raise AutenticacaoError("Credenciais inválidas")

        return self._gerar_token(usuario)

    def validar_token(self, token: str) -> Usuario:
        """
        Valida um token JWT.

        Args:
            token: Token JWT

        Returns:
            Usuário autenticado

        Raises:
            AutenticacaoError: Se o token for inválido
        """
        try:
            payload = jwt.decode(
                token,
                self._secret_key,
                algorithms=["HS256"],
            )
        except InvalidTokenError:
            raise AutenticacaoError("Token inválido")

        usuario = self._usuario_repository.buscar_por_id(payload["sub"])
        if not usuario:
            raise AutenticacaoError("Token inválido")

        if not usuario.ativo:
            raise AutenticacaoError("Usuário inativo")

        return usuario

    def _gerar_token(self, usuario: Usuario) -> str:
        """
        Gera um token JWT.

        Args:
            usuario: Usuário

        Returns:
            Token JWT
        """
        payload = {
            "sub": str(usuario.id),
            "email": str(usuario.email),
            "exp": datetime.utcnow() + timedelta(hours=self._token_expiration),
        }
        return jwt.encode(
            payload,
            self._secret_key,
            algorithm="HS256",
        )

    def _verificar_senha(self, senha: str, senha_hash: str) -> bool:
        """
        Verifica se a senha está correta.

        Args:
            senha: Senha em texto plano
            senha_hash: Hash da senha

        Returns:
            True se a senha estiver correta, False caso contrário
        """
        return bcrypt.checkpw(
            senha.encode("utf-8"),
            senha_hash.encode("utf-8"),
        )

    def gerar_hash_senha(self, senha: str) -> str:
        """
        Gera o hash de uma senha.

        Args:
            senha: Senha em texto plano

        Returns:
            Hash da senha
        """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(
            senha.encode("utf-8"),
            salt,
        ).decode("utf-8")
