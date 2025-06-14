"""
Serviço de aplicação para fornecedores.

Este módulo contém o serviço de aplicação que coordena as operações
relacionadas a fornecedores, fazendo a ponte entre a interface com o usuário
e o domínio.
"""
from typing import List, Optional

from ....domain.catalogo.entities.fornecedor import Documento, Fornecedor
from ....domain.catalogo.repositories.fornecedor_repository import FornecedorRepository
from ....domain.catalogo.services.fornecedor_service import FornecedorService
from ....domain.shared.value_objects.endereco import Endereco
from ..dtos.fornecedor_dto import (
    AtualizarFornecedorDTO,
    CriarFornecedorDTO,
    DocumentoDTO,
    EnderecoDTO,
    FornecedorDTO,
    ListagemFornecedorDTO,
)


class FornecedorAppService:
    """
    Serviço de aplicação para fornecedores.

    Esta classe implementa os casos de uso relacionados a fornecedores,
    coordenando as operações entre a interface com o usuário e o domínio.
    """

    def __init__(self, fornecedor_repository: FornecedorRepository):
        """
        Inicializa o serviço com suas dependências.

        Args:
            fornecedor_repository: Repositório de fornecedores
        """
        self._repository = fornecedor_repository
        self._service = FornecedorService(fornecedor_repository)

    def criar_fornecedor(self, dto: CriarFornecedorDTO) -> FornecedorDTO:
        """
        Cria um novo fornecedor.

        Args:
            dto: DTO com os dados do fornecedor

        Returns:
            FornecedorDTO: DTO com os dados do fornecedor criado

        Raises:
            ValueError: Se já existe um fornecedor com o mesmo documento
        """
        documento = Documento(numero=dto.documento_numero, tipo=dto.documento_tipo)

        endereco = self._to_endereco_entity(dto.endereco)

        fornecedor = self._service.criar_fornecedor(
            nome=dto.nome, documento=documento, endereco=endereco
        )

        return self._to_dto(fornecedor)

    def atualizar_fornecedor(
        self, fornecedor_id: int, dto: AtualizarFornecedorDTO
    ) -> Optional[FornecedorDTO]:
        """
        Atualiza um fornecedor existente.

        Args:
            fornecedor_id: ID do fornecedor
            dto: DTO com os dados a serem atualizados

        Returns:
            Optional[FornecedorDTO]: DTO com os dados do fornecedor atualizado
            ou None se não encontrado
        """
        fornecedor = self._repository.buscar_por_id(fornecedor_id)
        if not fornecedor:
            return None

        if dto.nome is not None:
            fornecedor.nome = dto.nome

        if dto.endereco is not None:
            endereco = self._to_endereco_entity(dto.endereco)
            fornecedor.atualizar_endereco(endereco)

        fornecedor = self._repository.atualizar(fornecedor)
        return self._to_dto(fornecedor)

    def buscar_por_id(self, fornecedor_id: int) -> Optional[FornecedorDTO]:
        """
        Busca um fornecedor pelo ID.

        Args:
            fornecedor_id: ID do fornecedor

        Returns:
            Optional[FornecedorDTO]: DTO com os dados do fornecedor ou None
        """
        fornecedor = self._repository.buscar_por_id(fornecedor_id)
        if not fornecedor:
            return None
        return self._to_dto(fornecedor)

    def listar(self, apenas_ativos: bool = True) -> List[ListagemFornecedorDTO]:
        """
        Lista todos os fornecedores.

        Args:
            apenas_ativos: Se True, retorna apenas fornecedores ativos

        Returns:
            List[ListagemFornecedorDTO]: Lista de DTOs com dados resumidos
            dos fornecedores
        """
        fornecedores = self._repository.listar(apenas_ativos)
        return [self._to_listagem_dto(f) for f in fornecedores]

    def buscar_por_nome(self, nome: str) -> List[ListagemFornecedorDTO]:
        """
        Busca fornecedores por nome.

        Args:
            nome: Nome ou parte do nome do fornecedor

        Returns:
            List[ListagemFornecedorDTO]: Lista de DTOs com dados resumidos
            dos fornecedores
        """
        fornecedores = self._service.buscar_por_nome(nome)
        return [self._to_listagem_dto(f) for f in fornecedores]

    def desativar_fornecedor(self, fornecedor_id: int) -> bool:
        """
        Desativa um fornecedor.

        Args:
            fornecedor_id: ID do fornecedor

        Returns:
            bool: True se desativado com sucesso, False caso contrário
        """
        return self._service.desativar_fornecedor(fornecedor_id)

    def ativar_fornecedor(self, fornecedor_id: int) -> bool:
        """
        Ativa um fornecedor.

        Args:
            fornecedor_id: ID do fornecedor

        Returns:
            bool: True se ativado com sucesso, False caso contrário
        """
        return self._service.ativar_fornecedor(fornecedor_id)

    def _to_dto(self, fornecedor: Fornecedor) -> FornecedorDTO:
        """
        Converte uma entidade Fornecedor para DTO.

        Args:
            fornecedor: A entidade a ser convertida

        Returns:
            FornecedorDTO: O DTO correspondente
        """
        return FornecedorDTO(
            nome=fornecedor.nome,
            documentos=[
                DocumentoDTO(numero=d.numero, tipo=d.tipo)
                for d in fornecedor.documentos
            ],
            endereco=EnderecoDTO(
                logradouro=fornecedor.endereco.logradouro,
                numero=fornecedor.endereco.numero,
                bairro=fornecedor.endereco.bairro,
                cidade=fornecedor.endereco.cidade,
                estado=fornecedor.endereco.estado,
                cep=fornecedor.endereco.cep,
                complemento=fornecedor.endereco.complemento,
                pais=fornecedor.endereco.pais,
            ),
            ativo=fornecedor.ativo,
        )

    def _to_listagem_dto(self, fornecedor: Fornecedor) -> ListagemFornecedorDTO:
        """
        Converte uma entidade Fornecedor para DTO de listagem.

        Args:
            fornecedor: A entidade a ser convertida

        Returns:
            ListagemFornecedorDTO: O DTO correspondente
        """
        return ListagemFornecedorDTO(
            nome=fornecedor.nome,
            documento_principal=DocumentoDTO(
                numero=fornecedor.documentos[0].numero,
                tipo=fornecedor.documentos[0].tipo,
            ),
            cidade=fornecedor.endereco.cidade,
            estado=fornecedor.endereco.estado,
            ativo=fornecedor.ativo,
        )

    def _to_endereco_entity(self, dto: EnderecoDTO) -> Endereco:
        """
        Converte um DTO de endereço para entidade.

        Args:
            dto: O DTO a ser convertido

        Returns:
            Endereco: A entidade correspondente
        """
        return Endereco(
            logradouro=dto.logradouro,
            numero=dto.numero,
            bairro=dto.bairro,
            cidade=dto.cidade,
            estado=dto.estado,
            cep=dto.cep,
            complemento=dto.complemento,
            pais=dto.pais,
        )
