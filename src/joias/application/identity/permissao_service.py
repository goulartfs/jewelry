"""
Serviço de aplicação para gerenciamento de permissões.
"""
from typing import List, Optional

from ...domain.entities.permissao import Permissao
from ...domain.repositories.permissao_repository import IPermissaoRepository
from ..dtos.permissao import CriarPermissaoDTO, PermissaoDTO, AtualizarPermissaoDTO


class PermissaoService:
    """
    Serviço de aplicação para gerenciamento de permissões.

    Esta classe implementa os casos de uso relacionados a permissões,
    como criação, consulta, atualização e remoção.
    """

    def __init__(self, permissao_repository: IPermissaoRepository):
        """
        Inicializa o serviço com suas dependências.

        Args:
            permissao_repository: Repositório de permissões
        """
        self._permissao_repository = permissao_repository

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
        # Normaliza a chave (maiúsculas)
        chave = dados.chave.upper()

        # Verifica se a chave já existe
        if self._permissao_repository.buscar_por_chave(chave):
            raise ValueError(f"Chave de permissão já cadastrada: {chave}")

        # Cria e persiste a permissão
        permissao = Permissao(
            nome=dados.nome,
            chave=chave,
            descricao=dados.descricao,
        )

        permissao = self._permissao_repository.criar(permissao)

        # Retorna o DTO
        return PermissaoDTO(
            id=str(permissao.id),
            nome=permissao.nome,
            chave=permissao.chave,
            descricao=permissao.descricao,
        )

    def atualizar_permissao(self, id: str, dados: AtualizarPermissaoDTO) -> PermissaoDTO:
        """
        Atualiza uma permissão existente.

        Args:
            id: ID da permissão
            dados: DTO com os dados a serem atualizados

        Returns:
            DTO com os dados da permissão atualizada

        Raises:
            ValueError: Se a permissão não existir ou os dados forem inválidos
        """
        # Busca a permissão
        permissao = self._permissao_repository.buscar_por_id(id)
        if not permissao:
            raise ValueError("Permissão não encontrada")

        # Verifica se a nova chave já existe (se foi fornecida)
        if dados.chave:
            chave = dados.chave.upper()
            permissao_existente = self._permissao_repository.buscar_por_chave(chave)
            if permissao_existente and permissao_existente.id != permissao.id:
                raise ValueError(f"Chave de permissão já cadastrada: {chave}")
            permissao.chave = chave

        # Atualiza o nome se fornecido
        if dados.nome is not None:
            permissao.nome = dados.nome

        # Atualiza a descrição se fornecida
        if dados.descricao is not None:
            permissao.descricao = dados.descricao

        # Atualiza a permissão
        permissao = self._permissao_repository.atualizar(permissao)

        # Retorna o DTO atualizado
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
        permissao = self._permissao_repository.buscar_por_id(id)

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
        permissoes = self._permissao_repository.listar()

        return [
            PermissaoDTO(
                id=str(p.id),
                nome=p.nome,
                chave=p.chave,
                descricao=p.descricao,
            )
            for p in permissoes
        ] 