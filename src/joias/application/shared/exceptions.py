"""
Exceções da aplicação.
"""


class EntidadeNaoEncontradaError(Exception):
    """
    Exceção lançada quando uma entidade não é encontrada.
    """

    pass


class EntidadeJaExisteError(Exception):
    """
    Exceção lançada quando uma entidade já existe.
    """

    pass


class ValidacaoError(Exception):
    """
    Exceção lançada quando há erro de validação.
    """

    pass


class AutenticacaoError(Exception):
    """
    Exceção lançada quando há erro de autenticação.
    """

    pass 