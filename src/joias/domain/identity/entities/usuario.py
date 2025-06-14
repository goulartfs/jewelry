"""
Entidade de usuário do sistema.

Esta classe representa um usuário do sistema, com suas informações
básicas e métodos de validação.
"""
from datetime import datetime
from typing import Optional

from ...shared.entities.aggregate_root import AggregateRoot
from ...shared.value_objects.email import Email


class Usuario(AggregateRoot):
    """
    Entidade que representa um usuário do sistema.
    
    Esta classe implementa as regras de negócio relacionadas
    ao usuário, incluindo validações e comportamentos.
    
    Attributes:
        nome: Nome completo do usuário
        email: Email do usuário (objeto de valor)
        senha_hashed: Hash da senha do usuário
        data_criacao: Data de criação do registro
        ativo: Status do usuário no sistema
    """
    
    def __init__(
        self,
        nome: str,
        email: Email,
        senha_hashed: str,
        data_criacao: Optional[datetime] = None,
        ativo: bool = True
    ) -> None:
        """
        Inicializa um novo usuário.
        
        Args:
            nome: Nome completo do usuário
            email: Email do usuário (objeto de valor)
            senha_hashed: Hash da senha do usuário
            data_criacao: Data de criação (opcional, default=now)
            ativo: Status do usuário (opcional, default=True)
            
        Raises:
            ValueError: Se o nome estiver vazio
        """
        super().__init__()
        
        if not nome or not nome.strip():
            raise ValueError("Nome do usuário não pode estar vazio")
            
        self._nome = nome.strip()
        self._email = email
        self._senha_hashed = senha_hashed
        self._data_criacao = data_criacao or datetime.now()
        self._ativo = ativo
        
    @property
    def nome(self) -> str:
        """Retorna o nome do usuário."""
        return self._nome
        
    @property
    def email(self) -> Email:
        """Retorna o email do usuário."""
        return self._email
        
    @property
    def senha_hashed(self) -> str:
        """Retorna o hash da senha do usuário."""
        return self._senha_hashed
        
    @property
    def data_criacao(self) -> datetime:
        """Retorna a data de criação do usuário."""
        return self._data_criacao
        
    @property
    def ativo(self) -> bool:
        """Retorna o status do usuário."""
        return self._ativo
        
    def desativar(self) -> None:
        """Desativa o usuário no sistema."""
        if not self._ativo:
            return
            
        self._ativo = False
        # TODO: Adicionar evento de domínio para usuário desativado
        
    def ativar(self) -> None:
        """Ativa o usuário no sistema."""
        if self._ativo:
            return
            
        self._ativo = True
        # TODO: Adicionar evento de domínio para usuário ativado 