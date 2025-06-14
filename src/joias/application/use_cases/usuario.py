"""
Casos de uso relacionados a usuários.

Este módulo contém os casos de uso para operações
relacionadas a usuários.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from ...domain.entities.usuario import Usuario
from ...domain.entities.empresa import Empresa
from ...domain.entities.autorizacao import Perfil
from ...domain.entities.dados_pessoais import DadoPessoal
from ...domain.repositories.usuario import UsuarioRepository
from .base import UseCase


@dataclass
class CriarUsuarioInput:
    """Dados de entrada para criação de usuário."""
    username: str
    email: str
    senha: str
    perfil: Perfil
    dados_pessoais: DadoPessoal
    empresa: Optional[Empresa] = None


class CriarUsuarioUseCase(UseCase[CriarUsuarioInput, Usuario]):
    """Caso de uso para criar um novo usuário."""

    def __init__(self, usuario_repository: UsuarioRepository):
        self.usuario_repository = usuario_repository

    def execute(self, input_data: CriarUsuarioInput) -> Usuario:
        """
        Executa o caso de uso.

        Args:
            input_data: Dados de entrada

        Returns:
            Usuário criado

        Raises:
            ValueError: Se o username ou email já existirem
        """
        if self.usuario_repository.buscar_por_username(input_data.username):
            raise ValueError("Username já existe")

        if self.usuario_repository.buscar_por_email(input_data.email):
            raise ValueError("Email já existe")

        usuario = Usuario(
            username=input_data.username,
            email=input_data.email,
            senha_hash=input_data.senha,  # TODO: Implementar hash da senha
            perfil=input_data.perfil,
            dados_pessoais=input_data.dados_pessoais,
            empresa=input_data.empresa,
            data_ultimo_acesso=datetime.now()
        )

        return self.usuario_repository.criar(usuario)


@dataclass
class AtualizarUsuarioInput:
    """Dados de entrada para atualização de usuário."""
    id: int
    email: Optional[str] = None
    senha: Optional[str] = None
    perfil: Optional[Perfil] = None
    dados_pessoais: Optional[DadoPessoal] = None
    empresa: Optional[Empresa] = None


class AtualizarUsuarioUseCase(UseCase[AtualizarUsuarioInput, Usuario]):
    """Caso de uso para atualizar um usuário existente."""

    def __init__(self, usuario_repository: UsuarioRepository):
        self.usuario_repository = usuario_repository

    def execute(self, input_data: AtualizarUsuarioInput) -> Usuario:
        """
        Executa o caso de uso.

        Args:
            input_data: Dados de entrada

        Returns:
            Usuário atualizado

        Raises:
            ValueError: Se o usuário não existir ou se o email já estiver em uso
        """
        usuario = self.usuario_repository.buscar_por_id(input_data.id)
        if not usuario:
            raise ValueError("Usuário não encontrado")

        if (
            input_data.email and
            input_data.email != usuario.email and
            self.usuario_repository.buscar_por_email(input_data.email)
        ):
            raise ValueError("Email já está em uso")

        if input_data.email:
            usuario.email = input_data.email
        if input_data.senha:
            usuario.senha_hash = input_data.senha  # TODO: Implementar hash da senha
        if input_data.perfil:
            usuario.perfil = input_data.perfil
        if input_data.dados_pessoais:
            usuario.dados_pessoais = input_data.dados_pessoais
        if input_data.empresa is not None:  # Permite desvincular empresa (None)
            usuario.empresa = input_data.empresa

        return self.usuario_repository.atualizar(usuario)


class DeletarUsuarioUseCase(UseCase[int, None]):
    """Caso de uso para deletar um usuário."""

    def __init__(self, usuario_repository: UsuarioRepository):
        self.usuario_repository = usuario_repository

    def execute(self, usuario_id: int) -> None:
        """
        Executa o caso de uso.

        Args:
            usuario_id: ID do usuário a ser deletado

        Raises:
            ValueError: Se o usuário não existir
        """
        usuario = self.usuario_repository.buscar_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuário não encontrado")

        self.usuario_repository.deletar(usuario)


class ListarUsuariosEmpresaUseCase(UseCase[int, List[Usuario]]):
    """Caso de uso para listar usuários de uma empresa."""

    def __init__(self, usuario_repository: UsuarioRepository):
        self.usuario_repository = usuario_repository

    def execute(self, empresa_id: int) -> List[Usuario]:
        """
        Executa o caso de uso.

        Args:
            empresa_id: ID da empresa

        Returns:
            Lista de usuários da empresa
        """
        return self.usuario_repository.buscar_por_empresa(empresa_id) 