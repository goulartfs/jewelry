"""
Serviços do módulo alpha.

Este módulo contém os serviços responsáveis por gerenciar as operações
relacionadas às entidades principais do sistema.
"""
from datetime import datetime
from typing import Generic, List, Optional, TypeVar

from .models import (
    Catalogo,
    Contato,
    DadoPessoal,
    Detalhe,
    Empresa,
    Endereco,
    ItemPedido,
    Pedido,
    Perfil,
    Permissao,
    Preco,
    Produto,
    Usuario,
    Variacao,
)

T = TypeVar("T")


class BaseService(Generic[T]):
    """
    Serviço base que implementa operações CRUD genéricas.
    """

    def __init__(self):
        self._items = {}
        self._next_id = 1

    def create(self, item: T) -> T:
        """
        Cria um novo item.

        Args:
            item: Item a ser criado

        Returns:
            T: Item criado com ID atualizado
        """
        setattr(item, "id", self._next_id)
        self._items[self._next_id] = item
        self._next_id += 1
        return item

    def get(self, item_id: int) -> Optional[T]:
        """
        Busca um item pelo ID.

        Args:
            item_id: ID do item

        Returns:
            Optional[T]: Item encontrado ou None
        """
        return self._items.get(item_id)

    def list(self, active_only: bool = True) -> List[T]:
        """
        Lista todos os itens.

        Args:
            active_only: Se True, retorna apenas itens ativos

        Returns:
            List[T]: Lista de itens
        """
        items = self._items.values()
        if active_only:
            return [item for item in items if getattr(item, "ativo", True)]
        return list(items)

    def update(self, item_id: int, item: T) -> Optional[T]:
        """
        Atualiza um item existente.

        Args:
            item_id: ID do item
            item: Item com dados atualizados

        Returns:
            Optional[T]: Item atualizado ou None se não encontrado
        """
        if item_id not in self._items:
            return None
        setattr(item, "id", item_id)
        self._items[item_id] = item
        return item

    def delete(self, item_id: int) -> bool:
        """
        Remove um item.

        Args:
            item_id: ID do item

        Returns:
            bool: True se removido com sucesso, False caso contrário
        """
        if item_id not in self._items:
            return False
        del self._items[item_id]
        return True

    def soft_delete(self, item_id: int) -> bool:
        """
        Marca um item como inativo.

        Args:
            item_id: ID do item

        Returns:
            bool: True se desativado com sucesso, False caso contrário
        """
        item = self.get(item_id)
        if not item:
            return False
        setattr(item, "ativo", False)
        return True


class UsuarioService(BaseService[Usuario]):
    """Serviço para gerenciamento de usuários."""

    def get_by_email(self, email: str) -> Optional[Usuario]:
        """
        Busca um usuário pelo email.

        Args:
            email: Email do usuário

        Returns:
            Optional[Usuario]: Usuário encontrado ou None
        """
        return next((u for u in self._items.values() if u.email == email), None)

    def get_by_username(self, username: str) -> Optional[Usuario]:
        """
        Busca um usuário pelo username.

        Args:
            username: Username do usuário

        Returns:
            Optional[Usuario]: Usuário encontrado ou None
        """
        return next((u for u in self._items.values() if u.username == username), None)

    def update_last_access(self, user_id: int) -> bool:
        """
        Atualiza a data do último acesso do usuário.

        Args:
            user_id: ID do usuário

        Returns:
            bool: True se atualizado com sucesso, False caso contrário
        """
        user = self.get(user_id)
        if not user:
            return False
        user.data_ultimo_acesso = datetime.now()
        return True


class ContatoService(BaseService[Contato]):
    """Serviço para gerenciamento de contatos."""

    def get_by_email(self, email: str) -> Optional[Contato]:
        """
        Busca um contato pelo email.

        Args:
            email: Email do contato

        Returns:
            Optional[Contato]: Contato encontrado ou None
        """
        return next((c for c in self._items.values() if c.email == email), None)


class DadoPessoalService(BaseService[DadoPessoal]):
    """Serviço para gerenciamento de dados pessoais."""

    def get_by_cpf(self, cpf: str) -> Optional[DadoPessoal]:
        """
        Busca dados pessoais pelo CPF.

        Args:
            cpf: CPF da pessoa

        Returns:
            Optional[DadoPessoal]: Dados pessoais encontrados ou None
        """
        return next((d for d in self._items.values() if d.cpf == cpf), None)


class EmpresaService(BaseService[Empresa]):
    """Serviço para gerenciamento de empresas."""

    def get_by_cnpj(self, cnpj: str) -> Optional[Empresa]:
        """
        Busca uma empresa pelo CNPJ.

        Args:
            cnpj: CNPJ da empresa

        Returns:
            Optional[Empresa]: Empresa encontrada ou None
        """
        return next((e for e in self._items.values() if e.cnpj == cnpj), None)


class PermissaoService(BaseService[Permissao]):
    """Serviço para gerenciamento de permissões."""

    def get_by_codigo(self, codigo: str) -> Optional[Permissao]:
        """
        Busca uma permissão pelo código.

        Args:
            codigo: Código da permissão

        Returns:
            Optional[Permissao]: Permissão encontrada ou None
        """
        return next((p for p in self._items.values() if p.codigo == codigo), None)


class PerfilService(BaseService[Perfil]):
    """Serviço para gerenciamento de perfis."""

    def add_permissao(self, perfil_id: int, permissao: Permissao) -> bool:
        """
        Adiciona uma permissão ao perfil.

        Args:
            perfil_id: ID do perfil
            permissao: Permissão a ser adicionada

        Returns:
            bool: True se adicionada com sucesso, False caso contrário
        """
        perfil = self.get(perfil_id)
        if not perfil:
            return False
        perfil.permissoes.append(permissao)
        return True

    def remove_permissao(self, perfil_id: int, permissao_id: int) -> bool:
        """
        Remove uma permissão do perfil.

        Args:
            perfil_id: ID do perfil
            permissao_id: ID da permissão

        Returns:
            bool: True se removida com sucesso, False caso contrário
        """
        perfil = self.get(perfil_id)
        if not perfil:
            return False

        for i, perm in enumerate(perfil.permissoes):
            if perm.id == permissao_id:
                perfil.permissoes.pop(i)
                return True
        return False


class ProdutoService(BaseService[Produto]):
    """Serviço para gerenciamento de produtos."""

    def get_by_codigo(self, codigo: str) -> Optional[Produto]:
        """
        Busca um produto pelo código.

        Args:
            codigo: Código do produto

        Returns:
            Optional[Produto]: Produto encontrado ou None
        """
        return next((p for p in self._items.values() if p.codigo == codigo), None)

    def add_variacao(self, produto_id: int, variacao: Variacao) -> bool:
        """
        Adiciona uma variação ao produto.

        Args:
            produto_id: ID do produto
            variacao: Variação a ser adicionada

        Returns:
            bool: True se adicionada com sucesso, False caso contrário
        """
        produto = self.get(produto_id)
        if not produto:
            return False
        produto.variacoes.append(variacao)
        return True

    def add_detalhe(self, produto_id: int, detalhe: Detalhe) -> bool:
        """
        Adiciona um detalhe ao produto.

        Args:
            produto_id: ID do produto
            detalhe: Detalhe a ser adicionado

        Returns:
            bool: True se adicionado com sucesso, False caso contrário
        """
        produto = self.get(produto_id)
        if not produto:
            return False
        produto.detalhes.append(detalhe)
        return True


class CatalogoService(BaseService[Catalogo]):
    """Serviço para gerenciamento de catálogos."""

    def get_by_usuario(self, usuario_id: int) -> List[Catalogo]:
        """
        Lista os catálogos de um usuário.

        Args:
            usuario_id: ID do usuário

        Returns:
            List[Catalogo]: Lista de catálogos do usuário
        """
        return [
            c for c in self._items.values() if c.usuario.id == usuario_id and c.ativo
        ]

    def add_produto(self, catalogo_id: int, produto: Produto) -> bool:
        """
        Adiciona um produto ao catálogo.

        Args:
            catalogo_id: ID do catálogo
            produto: Produto a ser adicionado

        Returns:
            bool: True se adicionado com sucesso, False caso contrário
        """
        catalogo = self.get(catalogo_id)
        if not catalogo:
            return False
        catalogo.produtos.append(produto)
        return True


class PedidoService(BaseService[Pedido]):
    """Serviço para gerenciamento de pedidos."""

    def get_by_usuario(self, usuario_id: int) -> List[Pedido]:
        """
        Lista os pedidos de um usuário.

        Args:
            usuario_id: ID do usuário

        Returns:
            List[Pedido]: Lista de pedidos do usuário
        """
        return [
            p for p in self._items.values() if p.usuario.id == usuario_id and p.ativo
        ]

    def add_item(self, pedido_id: int, item: ItemPedido) -> bool:
        """
        Adiciona um item ao pedido.

        Args:
            pedido_id: ID do pedido
            item: Item a ser adicionado

        Returns:
            bool: True se adicionado com sucesso, False caso contrário
        """
        pedido = self.get(pedido_id)
        if not pedido or pedido.status != "rascunho":
            return False
        pedido.itens.append(item)
        return True

    def confirmar_pedido(self, pedido_id: int) -> bool:
        """
        Confirma um pedido.

        Args:
            pedido_id: ID do pedido

        Returns:
            bool: True se confirmado com sucesso, False caso contrário
        """
        pedido = self.get(pedido_id)
        if not pedido or pedido.status != "rascunho" or not pedido.itens:
            return False
        pedido.status = "confirmado"
        pedido.data_confirmacao = datetime.now()
        return True

    def cancelar_pedido(self, pedido_id: int) -> bool:
        """
        Cancela um pedido.

        Args:
            pedido_id: ID do pedido

        Returns:
            bool: True se cancelado com sucesso, False caso contrário
        """
        pedido = self.get(pedido_id)
        if not pedido or pedido.status in ["cancelado", "entregue"]:
            return False
        pedido.status = "cancelado"
        pedido.data_cancelamento = datetime.now()
        return True
