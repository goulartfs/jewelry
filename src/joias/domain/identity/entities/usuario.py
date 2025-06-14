"""
Entidade de usuário.

Este módulo define a entidade de usuário do sistema,
que representa um usuário com suas credenciais e permissões.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from uuid import UUID

from ...shared.entities.aggregate_root import AggregateRoot
from ...shared.value_objects.email import Email
from .perfil import Perfil
from ...organization.entities.empresa import Empresa
from ...organization.value_objects.dados_pessoais import DadosPessoais


@dataclass
class Usuario(AggregateRoot):
    """
    Entidade de usuário.

    Esta classe representa um usuário do sistema, com seus
    dados pessoais, credenciais e permissões.

    Attributes:
        email: Email do usuário (identificador único)
        nome: Nome completo do usuário
        senha_hash: Hash da senha do usuário
        ativo: Se o usuário está ativo
        empresa_id: ID da empresa do usuário
        perfis: Lista de perfis do usuário
    """

    email: Email
    nome: str
    senha_hash: str
    ativo: bool = True
    empresa_id: Optional[UUID] = None
    perfis: List[UUID] = field(default_factory=list)
    dados_pessoais: DadosPessoais
    data_ultimo_acesso: Optional[datetime] = None
    id: UUID
    data_criacao: datetime

    def ativar(self) -> None:
        """Ativa o usuário."""
        if not self.ativo:
            self.ativo = True
            self.updated_at = datetime.utcnow()
            self.deleted_at = None

    def desativar(self) -> None:
        """Desativa o usuário."""
        if self.ativo:
            self.ativo = False
            self.updated_at = datetime.utcnow()
            self.deleted_at = datetime.utcnow()

    def adicionar_perfil(self, perfil_id: UUID) -> None:
        """
        Adiciona um perfil ao usuário.

        Args:
            perfil_id: ID do perfil
        """
        if perfil_id not in self.perfis:
            self.perfis.append(perfil_id)
            self.updated_at = datetime.utcnow()

    def remover_perfil(self, perfil_id: UUID) -> None:
        """
        Remove um perfil do usuário.

        Args:
            perfil_id: ID do perfil
        """
        if perfil_id in self.perfis:
            self.perfis.remove(perfil_id)
            self.updated_at = datetime.utcnow()

    def atualizar_email(self, novo_email: Email) -> None:
        """
        Atualiza o email do usuário.

        Args:
            novo_email: Novo email
        """
        if novo_email != self.email:
            self.email = novo_email
            self.updated_at = datetime.utcnow()

    def atualizar_nome(self, novo_nome: str) -> None:
        """
        Atualiza o nome do usuário.

        Args:
            novo_nome: Novo nome
        """
        if novo_nome != self.nome:
            self.nome = novo_nome
            self.updated_at = datetime.utcnow()

    def atualizar_senha(self, nova_senha_hash: str) -> None:
        """
        Atualiza a senha do usuário.

        Args:
            nova_senha_hash: Hash da nova senha
        """
        if nova_senha_hash != self.senha_hash:
            self.senha_hash = nova_senha_hash
            self.updated_at = datetime.utcnow()

    def vincular_empresa(self, empresa_id: UUID) -> None:
        """
        Vincula o usuário a uma empresa.

        Args:
            empresa_id: ID da empresa
        """
        if empresa_id != self.empresa_id:
            self.empresa_id = empresa_id
            self.updated_at = datetime.utcnow()

    def desvincular_empresa(self) -> None:
        """Desvincula o usuário da empresa atual."""
        if self.empresa_id is not None:
            self.empresa_id = None
            self.updated_at = datetime.utcnow()

    def registrar_acesso(self) -> None:
        """Registra um novo acesso do usuário."""
        self.data_ultimo_acesso = datetime.now()
        self.notificar_alteracao()

    def atualizar_dados_pessoais(self, dados: DadosPessoais) -> None:
        """
        Atualiza os dados pessoais do usuário.

        Args:
            dados: Novos dados pessoais
        """
        self.dados_pessoais = dados
        self.notificar_alteracao()

    def __str__(self) -> str:
        """Retorna uma representação legível do usuário."""
        status = "ativo" if self.ativo else "inativo"
        return f"{self.nome} ({self.email}) - {status}" 