"""
Serviço de aplicação para gerenciamento de permissões.
"""
from typing import List, Optional

from ...domain.entities.permissao import Permissao
from ...domain.repositories.permissao_repository import IPermissaoRepository
from ..dtos.permissao import CriarPermissaoDTO, PermissaoDTO


class PermissaoService:
    """
    Serviço de aplicação para gerenciamento de permissões.

    Esta classe implementa os casos de uso relacionados a permissões,
    como criação, consulta e remoção.
    """

    def __init__(self, permissao_repository: IPermissaoRepository):
        """
        Inicializa o serviço com suas dependências.

        Args:
            permissao_repository: Repositório de permissões
        """
        self._repository = permissao_repository

    def criar_permissao(self, dados: CriarPermissaoDTO) -> PermissaoDTO:
        """
        Cria uma nova permissão no sistema.

        Args:
            dados: DTO com os dados da permissão

        Returns:
            DTO com os dados da permissão criada

        Raises:
            ValueError: Se os dados forem inválidos ou a chave já existir
        """
        # Verifica se a chave já existe
        if self._repository.buscar_por_chave(dados.chave):
            raise ValueError(f"Chave de permissão já cadastrada: {dados.chave}")

        # Cria e persiste a permissão
        permissao = Permissao(
            nome=dados.nome,
            chave=dados.chave,
            descricao=dados.descricao,
        )

        permissao = self._repository.criar(permissao)

        # Retorna o DTO
        return PermissaoDTO(
            id=str(permissao.id),
            nome=permissao.nome,
            chave=permissao.chave,
            descricao=permissao.descricao,
        )

    def buscar_permissao(self, id: str) -> Optional[PermissaoDTO]:
        """
        Busca uma permissão pelo ID.

        Args:
            id: ID da permissão

        Returns:
            DTO com os dados da permissão ou None
        """
        permissao = self._repository.buscar_por_id(id)

        if not permissao:
            return None

        return PermissaoDTO(
            id=str(permissao.id),
            nome=permissao.nome,
            chave=permissao.chave,
            descricao=permissao.descricao,
        )

    def listar_permissoes(self) -> List[PermissaoDTO]:
        """
        Lista todas as permissões.

        Returns:
            Lista de DTOs de permissão
        """
        permissoes = self._repository.listar()

        return [
            PermissaoDTO(
                id=str(p.id),
                nome=p.nome,
                chave=p.chave,
                descricao=p.descricao,
            )
            for p in permissoes
        ] 