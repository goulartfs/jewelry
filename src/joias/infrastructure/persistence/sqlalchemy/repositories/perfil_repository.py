"""
Repositório SQLAlchemy para Perfil.
"""
import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from .....domain.entities.perfil import Perfil
from .....domain.entities.permissao import Permissao
from .....domain.repositories.perfil_repository import IPerfilRepository
from ..models.perfil import PerfilModel
from ..models.permissao import PermissaoModel


class SQLPerfilRepository(IPerfilRepository):
    """Implementação SQLAlchemy do repositório de Perfil."""

    def __init__(self, session: Session):
        """
        Inicializa o repositório.

        Args:
            session: Sessão do SQLAlchemy
        """
        self._session = session

    def criar(self, perfil: Perfil) -> Perfil:
        """
        Cria um novo perfil.

        Args:
            perfil: Perfil a ser criado

        Returns:
            Perfil criado com ID
        """
        # Cria o modelo
        model = PerfilModel(
            id=str(uuid.uuid4()),
            nome=perfil.nome,
            descricao=perfil.descricao,
            data_criacao=datetime.now(),
        )

        # Persiste
        self._session.add(model)
        self._session.commit()

        # Atualiza o ID da entidade
        perfil._id = model.id  # pylint: disable=protected-access

        return perfil

    def buscar_por_id(self, id: str) -> Optional[Perfil]:
        """
        Busca um perfil pelo ID.

        Args:
            id: ID do perfil

        Returns:
            Perfil encontrado ou None
        """
        model = self._session.query(PerfilModel).get(id)

        if not model:
            return None

        # Cria a entidade
        perfil = Perfil(
            nome=model.nome,
            descricao=model.descricao,
            data_criacao=model.data_criacao,
        )

        # Adiciona as permissões
        for permissao_model in model.permissoes:
            permissao = Permissao(
                nome=permissao_model.nome,
                chave=permissao_model.chave,
                descricao=permissao_model.descricao,
            )
            permissao._id = permissao_model.id  # pylint: disable=protected-access
            perfil.adicionar_permissao(permissao)

        # Atualiza o ID
        perfil._id = model.id  # pylint: disable=protected-access

        return perfil

    def buscar_por_nome(self, nome: str) -> Optional[Perfil]:
        """
        Busca um perfil pelo nome.

        Args:
            nome: Nome do perfil

        Returns:
            Perfil encontrado ou None
        """
        model = (
            self._session.query(PerfilModel)
            .filter(PerfilModel.nome == nome)
            .first()
        )

        if not model:
            return None

        # Cria a entidade
        perfil = Perfil(
            nome=model.nome,
            descricao=model.descricao,
            data_criacao=model.data_criacao,
        )

        # Adiciona as permissões
        for permissao_model in model.permissoes:
            permissao = Permissao(
                nome=permissao_model.nome,
                chave=permissao_model.chave,
                descricao=permissao_model.descricao,
            )
            permissao._id = permissao_model.id  # pylint: disable=protected-access
            perfil.adicionar_permissao(permissao)

        # Atualiza o ID
        perfil._id = model.id  # pylint: disable=protected-access

        return perfil

    def listar(self) -> List[Perfil]:
        """
        Lista todos os perfis.

        Returns:
            Lista de perfis
        """
        models = self._session.query(PerfilModel).all()

        perfis = []
        for model in models:
            # Cria a entidade
            perfil = Perfil(
                nome=model.nome,
                descricao=model.descricao,
                data_criacao=model.data_criacao,
            )

            # Adiciona as permissões
            for permissao_model in model.permissoes:
                permissao = Permissao(
                    nome=permissao_model.nome,
                    chave=permissao_model.chave,
                    descricao=permissao_model.descricao,
                )
                permissao._id = permissao_model.id  # pylint: disable=protected-access
                perfil.adicionar_permissao(permissao)

            # Atualiza o ID
            perfil._id = model.id  # pylint: disable=protected-access

            perfis.append(perfil)

        return perfis

    def atualizar(self, perfil: Perfil) -> Perfil:
        """
        Atualiza um perfil existente.

        Args:
            perfil: Perfil com as alterações

        Returns:
            Perfil atualizado
        """
        # Busca o modelo
        model = self._session.query(PerfilModel).get(perfil.id)

        if not model:
            raise ValueError("Perfil não encontrado")

        # Atualiza os dados básicos
        model.nome = perfil.nome
        model.descricao = perfil.descricao

        # Atualiza as permissões
        model.permissoes = []
        for permissao in perfil.permissoes:
            permissao_model = (
                self._session.query(PermissaoModel)
                .get(permissao.id)
            )
            if not permissao_model:
                raise ValueError(f"Permissão não encontrada: {permissao.id}")
            model.permissoes.append(permissao_model)

        # Persiste
        self._session.commit()

        return perfil

    def deletar(self, perfil: Perfil) -> None:
        """
        Remove um perfil.

        Args:
            perfil: Perfil a ser removido
        """
        model = self._session.query(PerfilModel).get(perfil.id)

        if model:
            self._session.delete(model)
            self._session.commit() 