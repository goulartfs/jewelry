"""
Serviço de usuário.
"""
from typing import List, Optional
from uuid import UUID

from ...domain.entities.usuario import Usuario
from ...domain.repositories.usuario_repository import IUsuarioRepository
from ...domain.shared.value_objects import Email
from ..shared.exceptions import (
    EntidadeJaExisteError,
    EntidadeNaoEncontradaError,
    ValidacaoError,
)
from .auth_service import AuthService


class UsuarioService:
    """
    Serviço para gerenciamento de usuários.
    """

    def __init__(
        self,
        usuario_repository: IUsuarioRepository,
        auth_service: AuthService,
    ):
        """
        Inicializa o serviço de usuário.

        Args:
            usuario_repository: Repositório de usuários
            auth_service: Serviço de autenticação
        """
        self._usuario_repository = usuario_repository
        self._auth_service = auth_service

    def criar_usuario(
        self,
        nome: str,
        email: str,
        senha: str,
    ) -> Usuario:
        """
        Cria um novo usuário.

        Args:
            nome: Nome do usuário
            email: Email do usuário
            senha: Senha do usuário

        Returns:
            Usuário criado

        Raises:
            EntidadeJaExisteError: Se já existe um usuário com o email informado
            ValidacaoError: Se os dados do usuário são inválidos
        """
        try:
            email_obj = Email(email)
        except ValueError as e:
            raise ValidacaoError(str(e))

        if self._usuario_repository.buscar_por_email(email_obj):
            raise EntidadeJaExisteError("Já existe um usuário com este email")

        senha_hash = self._auth_service.gerar_hash_senha(senha)

        usuario = Usuario(
            nome=nome,
            email=email_obj,
            senha_hash=senha_hash,
        )

        return self._usuario_repository.criar(usuario)

    def buscar_usuario_por_id(self, id: str) -> Usuario:
        """
        Busca um usuário pelo ID.

        Args:
            id: ID do usuário

        Returns:
            Usuário encontrado

        Raises:
            EntidadeNaoEncontradaError: Se o usuário não for encontrado
        """
        usuario = self._usuario_repository.buscar_por_id(id)
        if not usuario:
            raise EntidadeNaoEncontradaError("Usuário não encontrado")
        return usuario

    def buscar_usuario_por_email(self, email: str) -> Usuario:
        """
        Busca um usuário pelo email.

        Args:
            email: Email do usuário

        Returns:
            Usuário encontrado

        Raises:
            EntidadeNaoEncontradaError: Se o usuário não for encontrado
            ValidacaoError: Se o email for inválido
        """
        try:
            email_obj = Email(email)
        except ValueError as e:
            raise ValidacaoError(str(e))

        usuario = self._usuario_repository.buscar_por_email(email_obj)
        if not usuario:
            raise EntidadeNaoEncontradaError("Usuário não encontrado")
        return usuario

    def listar_usuarios(self) -> List[Usuario]:
        """
        Lista todos os usuários.

        Returns:
            Lista de usuários
        """
        return self._usuario_repository.listar()

    def atualizar_usuario(
        self,
        id: str,
        nome: Optional[str] = None,
        email: Optional[str] = None,
        senha: Optional[str] = None,
        ativo: Optional[bool] = None,
    ) -> Usuario:
        """
        Atualiza um usuário.

        Args:
            id: ID do usuário
            nome: Novo nome do usuário
            email: Novo email do usuário
            senha: Nova senha do usuário
            ativo: Novo status do usuário

        Returns:
            Usuário atualizado

        Raises:
            EntidadeNaoEncontradaError: Se o usuário não for encontrado
            EntidadeJaExisteError: Se já existe um usuário com o novo email
            ValidacaoError: Se os dados do usuário são inválidos
        """
        usuario = self.buscar_usuario_por_id(id)

        if nome is not None:
            usuario.nome = nome

        if email is not None:
            try:
                email_obj = Email(email)
            except ValueError as e:
                raise ValidacaoError(str(e))

            usuario_existente = self._usuario_repository.buscar_por_email(email_obj)
            if usuario_existente and usuario_existente.id != usuario.id:
                raise EntidadeJaExisteError("Já existe um usuário com este email")

            usuario.email = email_obj

        if senha is not None:
            usuario.senha_hash = self._auth_service.gerar_hash_senha(senha)

        if ativo is not None:
            usuario.ativo = ativo

        return self._usuario_repository.atualizar(usuario)

    def excluir_usuario(self, id: str) -> None:
        """
        Exclui um usuário.

        Args:
            id: ID do usuário

        Raises:
            EntidadeNaoEncontradaError: Se o usuário não for encontrado
        """
        usuario = self.buscar_usuario_por_id(id)
        self._usuario_repository.excluir(usuario) 