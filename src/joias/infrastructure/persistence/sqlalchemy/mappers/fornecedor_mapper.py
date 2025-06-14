"""
Mapeador para fornecedores.

Este módulo contém as funções de mapeamento entre as entidades de domínio
e os modelos SQLAlchemy para fornecedores.
"""
from typing import List

from .....domain.catalogo.entities.fornecedor import Fornecedor as FornecedorEntity
from .....domain.catalogo.entities.fornecedor import Documento as DocumentoEntity
from .....domain.shared.value_objects.endereco import Endereco
from ..models.fornecedor import Fornecedor as FornecedorModel
from ..models.fornecedor import Documento as DocumentoModel


def to_entity(model: FornecedorModel) -> FornecedorEntity:
    """
    Converte um modelo SQLAlchemy para uma entidade de domínio.

    Args:
        model: O modelo SQLAlchemy

    Returns:
        FornecedorEntity: A entidade de domínio correspondente
    """
    documentos = [
        DocumentoEntity(
            numero=d.numero,
            tipo=d.tipo
        )
        for d in model.documentos
    ]

    endereco = Endereco(
        logradouro=model.logradouro,
        numero=model.numero,
        bairro=model.bairro,
        cidade=model.cidade,
        estado=model.estado,
        cep=model.cep,
        complemento=model.complemento,
        pais=model.pais
    )

    fornecedor = FornecedorEntity(
        nome=model.nome,
        documentos=documentos,
        endereco=endereco
    )

    # Atributos que não fazem parte do construtor
    fornecedor.ativo = model.ativo

    return fornecedor


def to_model(entity: FornecedorEntity) -> FornecedorModel:
    """
    Converte uma entidade de domínio para um modelo SQLAlchemy.

    Args:
        entity: A entidade de domínio

    Returns:
        FornecedorModel: O modelo SQLAlchemy correspondente
    """
    model = FornecedorModel(
        nome=entity.nome,
        logradouro=entity.endereco.logradouro,
        numero=entity.endereco.numero,
        bairro=entity.endereco.bairro,
        cidade=entity.endereco.cidade,
        estado=entity.endereco.estado,
        cep=entity.endereco.cep,
        complemento=entity.endereco.complemento,
        pais=entity.endereco.pais,
        ativo=entity.ativo
    )

    model.documentos = [
        DocumentoModel(
            numero=d.numero,
            tipo=d.tipo
        )
        for d in entity.documentos
    ]

    return model


def update_model(model: FornecedorModel, entity: FornecedorEntity) -> None:
    """
    Atualiza um modelo SQLAlchemy com os dados de uma entidade.

    Args:
        model: O modelo SQLAlchemy a ser atualizado
        entity: A entidade com os dados atualizados
    """
    model.nome = entity.nome
    model.logradouro = entity.endereco.logradouro
    model.numero = entity.endereco.numero
    model.bairro = entity.endereco.bairro
    model.cidade = entity.endereco.cidade
    model.estado = entity.endereco.estado
    model.cep = entity.endereco.cep
    model.complemento = entity.endereco.complemento
    model.pais = entity.endereco.pais
    model.ativo = entity.ativo

    # Atualiza documentos
    # Remove documentos que não existem mais na entidade
    model.documentos = [
        d for d in model.documentos
        if any(
            d.numero == ed.numero and d.tipo == ed.tipo
            for ed in entity.documentos
        )
    ]

    # Adiciona novos documentos
    for doc_entity in entity.documentos:
        if not any(
            d.numero == doc_entity.numero and d.tipo == doc_entity.tipo
            for d in model.documentos
        ):
            model.documentos.append(
                DocumentoModel(
                    numero=doc_entity.numero,
                    tipo=doc_entity.tipo
                )
            ) 