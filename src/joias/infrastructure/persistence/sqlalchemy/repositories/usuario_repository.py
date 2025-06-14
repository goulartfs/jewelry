"""
Implementação SQLAlchemy do repositório de usuários.

Este módulo implementa o repositório de usuários usando
SQLAlchemy como ORM para persistência.
"""
from typing import List, Optional
from uuid import uuid4

from sqlalchemy import or_
from sqlalchemy.orm import Session

from .....domain.identity.entities.usuario import Usuario
from .....domain.identity.repositories.usuario_repository import IUsuarioRepository
from .....domain.shared.value_objects.email import Email
from ..models.usuario import UsuarioModel


class SQLUsuarioRepository(IUsuarioRepository):
    """
    Implementação SQLAlchemy do repositório de usuários.

    Esta classe implementa a interface IUsuarioRepository usando
    SQLAlchemy para persistência dos dados.
    """

    def __init__(self, session: Session):
        """
        Inicializa o repositório com uma sessão do SQLAlchemy.

        Args:
            session: Sessão do SQLAlchemy
        """
        self._session = session

    def criar(self, usuario: Usuario) -> Usuario:
        """
        Persiste um novo usuário.

        Args:
            usuario: O usuário a ser persistido

        Returns:
            O usuário persistido

        Raises:
            ValueError: Se o email já existir
        """
        # Verifica se o email já existe
        if self.buscar_por_email(usuario.email):
            raise ValueError(f"Email já cadastrado: {usuario.email}")

        # Cria o modelo
        model = UsuarioModel(
            id=str(uuid4()),
            nome=usuario.nome,
            email=str(usuario.email),
            senha_hashed=usuario.senha_hashed,
            data_criacao=usuario.data_criacao,
            ativo=usuario.ativo,
        )

        # Persiste
        self._session.add(model)
        self._session.commit()

        # Retorna o usuário
        return self._to_entity(model)

    def buscar_por_id(self, id: str) -> Optional[Usuario]:
        """
        Busca um usuário pelo seu ID.

        Args:
            id: O ID do usuário

        Returns:
            O usuário encontrado ou None
        """
        model = self._session.query(UsuarioModel).get(id)

        if not model:
            return None

        return self._to_entity(model)

    def buscar_por_email(self, email: Email) -> Optional[Usuario]:
        """
        Busca um usuário pelo seu email.

        Args:
            email: O email do usuário

        Returns:
            O usuário encontrado ou None
        """
        model = (
            self._session.query(UsuarioModel)
            .filter(UsuarioModel.email == str(email))
            .first()
        )

        if not model:
            return None

        return self._to_entity(model)

    def listar(
        self,
        pagina: int = 1,
        tamanho: int = 10,
        email: Optional[str] = None,
        nome: Optional[str] = None,
    ) -> List[Usuario]:
        """
        Lista usuários com paginação e filtros opcionais.

        Args:
            pagina: Número da página (1-based)
            tamanho: Tamanho da página
            email: Filtro por email
            nome: Filtro por nome

        Returns:
            Lista de usuários
        """
        query = self._session.query(UsuarioModel)

        # Aplica filtros
        if email or nome:
            query = query.filter(
                or_(
                    UsuarioModel.email.ilike(f"%{email}%") if email else False,
                    UsuarioModel.nome.ilike(f"%{nome}%") if nome else False,
                )
            )

        # Aplica paginação
        offset = (pagina - 1) * tamanho
        query = query.offset(offset).limit(tamanho)

        # Converte para entidades
        return [self._to_entity(model) for model in query.all()]

    def atualizar(self, usuario: Usuario) -> Usuario:
        """
        Atualiza um usuário existente.

        Args:
            usuario: O usuário com as alterações

        Returns:
            O usuário atualizado

        Raises:
            ValueError: Se o usuário não existir
        """
        model = self._session.query(UsuarioModel).get(str(usuario.id))

        if not model:
            raise ValueError(f"Usuário não encontrado: {usuario.id}")

        # Atualiza os campos
        model.nome = usuario.nome
        model.email = str(usuario.email)
        model.senha_hashed = usuario.senha_hashed
        model.ativo = usuario.ativo

        # Persiste
        self._session.commit()

        return self._to_entity(model)

    def excluir(self, id: str) -> None:
        """
        Remove um usuário do repositório.

        Args:
            id: O ID do usuário

        Raises:
            ValueError: Se o usuário não existir
        """
        model = self._session.query(UsuarioModel).get(id)

        if not model:
            raise ValueError(f"Usuário não encontrado: {id}")

        self._session.delete(model)
        self._session.commit()

    def _to_entity(self, model: UsuarioModel) -> Usuario:
        """
        Converte um modelo SQLAlchemy para uma entidade de domínio.

        Args:
            model: O modelo SQLAlchemy

        Returns:
            A entidade de domínio
        """
        return Usuario(
            nome=model.nome,
            email=Email(model.email),
            senha_hashed=model.senha_hashed,
            data_criacao=model.data_criacao,
            ativo=model.ativo,
        )
