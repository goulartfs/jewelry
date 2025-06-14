"""
Repositório SQLAlchemy para Permissão.
"""
import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from .....domain.entities.permissao import Permissao
from .....domain.repositories.permissao_repository import IPermissaoRepository
from ..models.permissao import PermissaoModel


class SQLPermissaoRepository(IPermissaoRepository):
    """Implementação SQLAlchemy do repositório de Permissão."""

    def __init__(self, session: Session):
        """
        Inicializa o repositório.

        Args:
            session: Sessão do SQLAlchemy
        """
        self._session = session

    def criar(self, permissao: Permissao) -> Permissao:
        """
        Cria uma nova permissão.

        Args:
            permissao: Permissão a ser criada

        Returns:
            Permissão criada com ID
        """
        # Cria o modelo
        model = PermissaoModel(
            id=str(uuid.uuid4()),
            nome=permissao.nome,
            chave=permissao.chave,
            descricao=permissao.descricao,
        )

        # Persiste
        self._session.add(model)
        self._session.commit()

        # Atualiza o ID da entidade
        permissao._id = model.id  # pylint: disable=protected-access

        return permissao

    def buscar_por_id(self, id: str) -> Optional[Permissao]:
        """
        Busca uma permissão pelo ID.

        Args:
            id: ID da permissão

        Returns:
            Permissão encontrada ou None
        """
        model = self._session.query(PermissaoModel).get(id)

        if not model:
            return None

        return Permissao(
            nome=model.nome,
            chave=model.chave,
            descricao=model.descricao,
        )

    def buscar_por_chave(self, chave: str) -> Optional[Permissao]:
        """
        Busca uma permissão pela chave.

        Args:
            chave: Chave da permissão

        Returns:
            Permissão encontrada ou None
        """
        model = (
            self._session.query(PermissaoModel)
            .filter(PermissaoModel.chave == chave.upper())
            .first()
        )

        if not model:
            return None

        return Permissao(
            nome=model.nome,
            chave=model.chave,
            descricao=model.descricao,
        )

    def listar(self) -> List[Permissao]:
        """
        Lista todas as permissões.

        Returns:
            Lista de permissões
        """
        models = self._session.query(PermissaoModel).all()

        return [
            Permissao(
                nome=model.nome,
                chave=model.chave,
                descricao=model.descricao,
            )
            for model in models
        ]

    def deletar(self, permissao: Permissao) -> None:
        """
        Remove uma permissão.

        Args:
            permissao: Permissão a ser removida
        """
        model = self._session.query(PermissaoModel).get(permissao.id)

        if model:
            self._session.delete(model)
            self._session.commit() 