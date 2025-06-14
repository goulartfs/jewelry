"""
Entidade de usuário.

Este módulo contém a entidade de usuário e suas classes relacionadas.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

from .base import Entity
from .autorizacao import Perfil
from .dados_pessoais import DadoPessoal
from .empresa import Empresa


@dataclass
class Usuario(Entity):
    """
    Entidade que representa um usuário do sistema.
    
    Um usuário é uma pessoa que interage com o sistema e pode
    ter diferentes níveis de acesso baseados em seu perfil.
    """
    username: str
    email: str
    senha_hash: str
    perfil: Perfil
    dados_pessoais: DadoPessoal
    empresa: Optional[Empresa] = None
    data_ultimo_acesso: Optional[datetime] = None

    def atualizar_ultimo_acesso(self) -> None:
        """Atualiza a data do último acesso do usuário."""
        self.data_ultimo_acesso = datetime.now()
        self.atualizar()

    def alterar_senha(self, nova_senha_hash: str) -> None:
        """
        Altera a senha do usuário.

        Args:
            nova_senha_hash: Nova senha já hasheada
        """
        self.senha_hash = nova_senha_hash
        self.atualizar()

    def vincular_empresa(self, empresa: Empresa) -> None:
        """
        Vincula uma empresa ao usuário.

        Args:
            empresa: Empresa a ser vinculada
        """
        self.empresa = empresa
        self.atualizar()

    def desvincular_empresa(self) -> None:
        """Remove o vínculo com a empresa atual."""
        self.empresa = None
        self.atualizar()

    def tem_permissao(self, codigo_permissao: str) -> bool:
        """
        Verifica se o usuário tem uma determinada permissão.

        Args:
            codigo_permissao: Código da permissão a ser verificada

        Returns:
            True se o usuário tem a permissão, False caso contrário
        """
        return any(
            p.codigo == codigo_permissao
            for p in self.perfil.permissoes
        ) 