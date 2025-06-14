"""
Serviço de aplicação para gerenciamento de usuários.

Este módulo implementa os casos de uso relacionados a usuários,
orquestrando as operações entre a API e o domínio.
"""
from dataclasses import dataclass
from typing import List, Optional

import bcrypt

from ...domain.identity.entities.usuario import Usuario
from ...domain.identity.repositories.usuario_repository import IUsuarioRepository
from ...domain.shared.value_objects.email import Email


@dataclass
class CriarUsuarioDTO:
    """DTO para criação de usuário."""

    nome: str
    email: str
    senha: str


@dataclass
class AtualizarUsuarioDTO:
    """DTO para atualização de usuário."""

    id: str
    nome: Optional[str] = None
    email: Optional[str] = None
    ativo: Optional[bool] = None


@dataclass
class UsuarioDTO:
    """DTO para retorno de usuário."""

    id: str
    nome: str
    email: str
    ativo: bool
    data_criacao: str


class UserService:
    """
    Serviço de aplicação para gerenciamento de usuários.

    Esta classe implementa os casos de uso relacionados a usuários,
    como criação, consulta, atualização e remoção.
    """

    def __init__(self, usuario_repository: IUsuarioRepository):
        """
        Inicializa o serviço com suas dependências.

        Args:
            usuario_repository: Repositório de usuários
        """
        self._repository = usuario_repository

    def criar_usuario(self, dados: CriarUsuarioDTO) -> UsuarioDTO:
        """
        Cria um novo usuário no sistema.

        Este método implementa o caso de uso US1, realizando:
        1. Validação dos dados de entrada
        2. Verificação de unicidade do email
        3. Hash da senha
        4. Persistência do usuário

        Args:
            dados: DTO com os dados do usuário

        Returns:
            DTO com os dados do usuário criado

        Raises:
            ValueError: Se os dados forem inválidos ou o email já existir
        """
        # Cria o objeto de valor Email (já valida o formato)
        email = Email(dados.email)

        # Verifica se o email já existe
        if self._repository.buscar_por_email(email):
            raise ValueError(f"Email já cadastrado: {dados.email}")

        # Gera o hash da senha
        senha_hashed = bcrypt.hashpw(
            dados.senha.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        # Cria e persiste o usuário
        usuario = Usuario(nome=dados.nome, email=email, senha_hashed=senha_hashed)

        usuario = self._repository.criar(usuario)

        # Retorna o DTO
        return UsuarioDTO(
            id=str(usuario.id),
            nome=usuario.nome,
            email=str(usuario.email),
            ativo=usuario.ativo,
            data_criacao=usuario.data_criacao.isoformat(),
        )

    def buscar_usuario(self, id: str) -> Optional[UsuarioDTO]:
        """
        Busca um usuário pelo ID.

        Args:
            id: ID do usuário

        Returns:
            DTO com os dados do usuário ou None
        """
        usuario = self._repository.buscar_por_id(id)

        if not usuario:
            return None

        return UsuarioDTO(
            id=str(usuario.id),
            nome=usuario.nome,
            email=str(usuario.email),
            ativo=usuario.ativo,
            data_criacao=usuario.data_criacao.isoformat(),
        )

    def listar_usuarios(
        self,
        pagina: int = 1,
        tamanho: int = 10,
        email: Optional[str] = None,
        nome: Optional[str] = None,
    ) -> List[UsuarioDTO]:
        """
        Lista usuários com paginação e filtros opcionais.

        Args:
            pagina: Número da página
            tamanho: Tamanho da página
            email: Filtro por email
            nome: Filtro por nome

        Returns:
            Lista de DTOs de usuário
        """
        usuarios = self._repository.listar(
            pagina=pagina, tamanho=tamanho, email=email, nome=nome
        )

        return [
            UsuarioDTO(
                id=str(u.id),
                nome=u.nome,
                email=str(u.email),
                ativo=u.ativo,
                data_criacao=u.data_criacao.isoformat(),
            )
            for u in usuarios
        ]

    def atualizar_usuario(self, dto: AtualizarUsuarioDTO) -> UsuarioDTO:
        """
        Atualiza um usuário existente.
        
        Args:
            dto: Dados do usuário a ser atualizado
            
        Returns:
            UsuarioDTO com os dados do usuário atualizado
            
        Raises:
            ValueError: Se o usuário não existir ou se o email já estiver em uso
        """
        # Busca o usuário
        usuario = self._repository.buscar_por_id(dto.id)
        if not usuario:
            raise ValueError("Usuário não encontrado")
        
        # Atualiza os campos fornecidos
        if dto.nome is not None:
            usuario.nome = dto.nome
        
        if dto.email is not None:
            novo_email = Email(dto.email)
            if str(novo_email) != str(usuario.email):
                # Verifica se o novo email já está em uso
                existente = self._repository.buscar_por_email(novo_email)
                if existente and existente.id != usuario.id:
                    raise ValueError("Email já cadastrado")
                usuario.email = novo_email
        
        if dto.ativo is not None:
            if dto.ativo:
                usuario.ativar()
            else:
                usuario.desativar()
        
        # Persiste e retorna
        atualizado = self._repository.atualizar(usuario)
        return UsuarioDTO(
            id=str(atualizado.id),
            nome=atualizado.nome,
            email=str(atualizado.email),
            ativo=atualizado.ativo,
            data_criacao=str(atualizado.data_criacao)
        )
