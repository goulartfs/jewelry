"""
Serviço de aplicação para gerenciamento de perfis.
"""
from typing import List, Optional

from ...domain.entities.perfil import Perfil
from ...domain.entities.permissao import Permissao
from ...domain.repositories.perfil_repository import IPerfilRepository
from ...domain.repositories.permissao_repository import IPermissaoRepository
from ..dtos.perfil import CriarPerfilDTO, PerfilDTO, AtualizarPerfilDTO
from ..dtos.permissao import PermissaoDTO


class PerfilService:
    """
    Serviço de aplicação para gerenciamento de perfis.

    Esta classe implementa os casos de uso relacionados a perfis,
    como criação, consulta, atualização e remoção.
    """

    def __init__(
        self,
        perfil_repository: IPerfilRepository,
        permissao_repository: IPermissaoRepository,
    ):
        """
        Inicializa o serviço com suas dependências.

        Args:
            perfil_repository: Repositório de perfis
            permissao_repository: Repositório de permissões
        """
        self._perfil_repository = perfil_repository
        self._permissao_repository = permissao_repository

    def criar_perfil(self, dados: CriarPerfilDTO) -> PerfilDTO:
        """
        Cria um novo perfil no sistema.

        Args:
            dados: DTO com os dados do perfil

        Returns:
            DTO com os dados do perfil criado

        Raises:
            ValueError: Se os dados forem inválidos ou o nome já existir
        """
        # Verifica se o nome já existe
        if self._perfil_repository.buscar_por_nome(dados.nome):
            raise ValueError(f"Nome de perfil já cadastrado: {dados.nome}")

        # Cria e persiste o perfil
        perfil = Perfil(
            nome=dados.nome,
            descricao=dados.descricao,
        )

        perfil = self._perfil_repository.criar(perfil)

        # Retorna o DTO
        return PerfilDTO(
            id=str(perfil.id),
            nome=perfil.nome,
            descricao=perfil.descricao,
            permissoes=[],
            data_criacao=perfil.data_criacao,
        )

    def atualizar_perfil(self, id: str, dados: AtualizarPerfilDTO) -> PerfilDTO:
        """
        Atualiza um perfil existente.

        Args:
            id: ID do perfil
            dados: DTO com os dados a serem atualizados

        Returns:
            DTO com os dados do perfil atualizado

        Raises:
            ValueError: Se o perfil não existir ou os dados forem inválidos
        """
        # Busca o perfil
        perfil = self._perfil_repository.buscar_por_id(id)
        if not perfil:
            raise ValueError("Perfil não encontrado")

        # Verifica se o novo nome já existe (se foi fornecido)
        if dados.nome and dados.nome != perfil.nome:
            perfil_existente = self._perfil_repository.buscar_por_nome(dados.nome)
            if perfil_existente:
                raise ValueError(f"Nome de perfil já cadastrado: {dados.nome}")
            perfil.nome = dados.nome

        # Atualiza a descrição se fornecida
        if dados.descricao is not None:
            perfil.descricao = dados.descricao

        # Atualiza o perfil
        perfil = self._perfil_repository.atualizar(perfil)

        # Retorna o DTO atualizado
        return PerfilDTO(
            id=str(perfil.id),
            nome=perfil.nome,
            descricao=perfil.descricao,
            permissoes=[
                PermissaoDTO(
                    id=str(p.id),
                    nome=p.nome,
                    chave=p.chave,
                    descricao=p.descricao,
                )
                for p in perfil.permissoes
            ],
            data_criacao=perfil.data_criacao,
        )

    def buscar_perfil(self, id: str) -> Optional[PerfilDTO]:
        """
        Busca um perfil pelo ID.

        Args:
            id: ID do perfil

        Returns:
            DTO com os dados do perfil ou None
        """
        perfil = self._perfil_repository.buscar_por_id(id)

        if not perfil:
            return None

        return PerfilDTO(
            id=str(perfil.id),
            nome=perfil.nome,
            descricao=perfil.descricao,
            permissoes=[
                PermissaoDTO(
                    id=str(p.id),
                    nome=p.nome,
                    chave=p.chave,
                    descricao=p.descricao,
                )
                for p in perfil.permissoes
            ],
            data_criacao=perfil.data_criacao,
        )

    def listar_perfis(self) -> List[PerfilDTO]:
        """
        Lista todos os perfis.

        Returns:
            Lista de DTOs de perfil
        """
        perfis = self._perfil_repository.listar()

        return [
            PerfilDTO(
                id=str(p.id),
                nome=p.nome,
                descricao=p.descricao,
                permissoes=[
                    PermissaoDTO(
                        id=str(perm.id),
                        nome=perm.nome,
                        chave=perm.chave,
                        descricao=perm.descricao,
                    )
                    for perm in p.permissoes
                ],
                data_criacao=p.data_criacao,
            )
            for p in perfis
        ]

    def adicionar_permissao(self, perfil_id: str, permissao_id: str) -> PerfilDTO:
        """
        Adiciona uma permissão a um perfil.

        Args:
            perfil_id: ID do perfil
            permissao_id: ID da permissão

        Returns:
            DTO com os dados do perfil atualizado

        Raises:
            ValueError: Se o perfil ou a permissão não existirem
        """
        # Busca o perfil e a permissão
        perfil = self._perfil_repository.buscar_por_id(perfil_id)
        if not perfil:
            raise ValueError("Perfil não encontrado")

        permissao = self._permissao_repository.buscar_por_id(permissao_id)
        if not permissao:
            raise ValueError("Permissão não encontrada")

        # Adiciona a permissão ao perfil
        perfil.adicionar_permissao(permissao)

        # Atualiza o perfil
        perfil = self._perfil_repository.atualizar(perfil)

        # Retorna o DTO atualizado
        return PerfilDTO(
            id=str(perfil.id),
            nome=perfil.nome,
            descricao=perfil.descricao,
            permissoes=[
                PermissaoDTO(
                    id=str(p.id),
                    nome=p.nome,
                    chave=p.chave,
                    descricao=p.descricao,
                )
                for p in perfil.permissoes
            ],
            data_criacao=perfil.data_criacao,
        )

    def remover_permissao(self, perfil_id: str, permissao_id: str) -> PerfilDTO:
        """
        Remove uma permissão de um perfil.

        Args:
            perfil_id: ID do perfil
            permissao_id: ID da permissão

        Returns:
            DTO com os dados do perfil atualizado

        Raises:
            ValueError: Se o perfil ou a permissão não existirem
        """
        # Busca o perfil e a permissão
        perfil = self._perfil_repository.buscar_por_id(perfil_id)
        if not perfil:
            raise ValueError("Perfil não encontrado")

        permissao = self._permissao_repository.buscar_por_id(permissao_id)
        if not permissao:
            raise ValueError("Permissão não encontrada")

        # Remove a permissão do perfil
        perfil.remover_permissao(permissao)

        # Atualiza o perfil
        perfil = self._perfil_repository.atualizar(perfil)

        # Retorna o DTO atualizado
        return PerfilDTO(
            id=str(perfil.id),
            nome=perfil.nome,
            descricao=perfil.descricao,
            permissoes=[
                PermissaoDTO(
                    id=str(p.id),
                    nome=p.nome,
                    chave=p.chave,
                    descricao=p.descricao,
                )
                for p in perfil.permissoes
            ],
            data_criacao=perfil.data_criacao,
        )

    def excluir_perfil(self, id: str) -> None:
        """
        Exclui um perfil do sistema.

        Args:
            id: ID do perfil

        Raises:
            ValueError: Se o perfil não existir ou não puder ser excluído
        """
        # Busca o perfil
        perfil = self._perfil_repository.buscar_por_id(id)
        if not perfil:
            raise ValueError("Perfil não encontrado")

        # Verifica se o perfil pode ser excluído
        if perfil.permissoes:
            raise ValueError("Não é possível excluir um perfil que possui permissões associadas")

        # Exclui o perfil
        self._perfil_repository.excluir(perfil) 