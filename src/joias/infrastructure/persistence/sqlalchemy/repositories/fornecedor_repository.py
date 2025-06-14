"""
Implementação SQLAlchemy do repositório de fornecedores.

Este módulo contém a implementação concreta do repositório de fornecedores
usando SQLAlchemy como ORM.
"""
from typing import List, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from .....domain.catalogo.entities.fornecedor import Documento as DocumentoEntity
from .....domain.catalogo.entities.fornecedor import Fornecedor as FornecedorEntity
from .....domain.catalogo.repositories.fornecedor_repository import FornecedorRepository
from ..mappers.fornecedor_mapper import to_entity, to_model, update_model
from ..models.fornecedor import Documento as DocumentoModel
from ..models.fornecedor import Fornecedor as FornecedorModel


class SQLAlchemyFornecedorRepository(FornecedorRepository):
    """
    Implementação SQLAlchemy do repositório de fornecedores.

    Esta classe implementa a interface FornecedorRepository usando
    SQLAlchemy como ORM para persistência dos dados.
    """

    def __init__(self, session: Session):
        """
        Inicializa o repositório com uma sessão SQLAlchemy.

        Args:
            session: Sessão SQLAlchemy
        """
        self._session = session

    def salvar(self, fornecedor: FornecedorEntity) -> FornecedorEntity:
        """
        Salva um fornecedor no banco de dados.

        Args:
            fornecedor: O fornecedor a ser salvo

        Returns:
            FornecedorEntity: O fornecedor salvo com ID atualizado
        """
        model = to_model(fornecedor)
        self._session.add(model)
        self._session.flush()  # Para gerar o ID
        return to_entity(model)

    def buscar_por_id(self, fornecedor_id: int) -> Optional[FornecedorEntity]:
        """
        Busca um fornecedor pelo ID.

        Args:
            fornecedor_id: ID do fornecedor

        Returns:
            Optional[FornecedorEntity]: O fornecedor encontrado ou None
        """
        model = self._session.query(FornecedorModel).get(fornecedor_id)
        if not model:
            return None
        return to_entity(model)

    def buscar_por_documento(
        self, documento: DocumentoEntity
    ) -> Optional[FornecedorEntity]:
        """
        Busca um fornecedor pelo documento.

        Args:
            documento: Documento do fornecedor

        Returns:
            Optional[FornecedorEntity]: O fornecedor encontrado ou None
        """
        model = (
            self._session.query(FornecedorModel)
            .join(FornecedorModel.documentos)
            .filter(
                DocumentoModel.numero == documento.numero,
                DocumentoModel.tipo == documento.tipo,
            )
            .first()
        )
        if not model:
            return None
        return to_entity(model)

    def listar(self, apenas_ativos: bool = True) -> List[FornecedorEntity]:
        """
        Lista todos os fornecedores.

        Args:
            apenas_ativos: Se True, retorna apenas fornecedores ativos

        Returns:
            List[FornecedorEntity]: Lista de fornecedores
        """
        query = self._session.query(FornecedorModel)
        if apenas_ativos:
            query = query.filter(FornecedorModel.ativo == True)
        return [to_entity(model) for model in query.all()]

    def buscar_por_nome(self, nome: str) -> List[FornecedorEntity]:
        """
        Busca fornecedores por nome.

        Args:
            nome: Nome ou parte do nome do fornecedor

        Returns:
            List[FornecedorEntity]: Lista de fornecedores encontrados
        """
        models = (
            self._session.query(FornecedorModel)
            .filter(FornecedorModel.nome.ilike(f"%{nome}%"))
            .all()
        )
        return [to_entity(model) for model in models]

    def atualizar(self, fornecedor: FornecedorEntity) -> Optional[FornecedorEntity]:
        """
        Atualiza um fornecedor existente.

        Args:
            fornecedor: O fornecedor com dados atualizados

        Returns:
            Optional[FornecedorEntity]: O fornecedor atualizado ou None
            se não encontrado
        """
        model = self._session.query(FornecedorModel).get(fornecedor.id)
        if not model:
            return None

        update_model(model, fornecedor)
        self._session.flush()
        return to_entity(model)

    def excluir(self, fornecedor_id: int) -> bool:
        """
        Remove um fornecedor.

        Args:
            fornecedor_id: ID do fornecedor

        Returns:
            bool: True se removido com sucesso, False caso contrário
        """
        model = self._session.query(FornecedorModel).get(fornecedor_id)
        if not model:
            return False

        self._session.delete(model)
        return True
