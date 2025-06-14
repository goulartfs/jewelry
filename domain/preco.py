import moeda


class Preco:
    """
    Representa um valor monetário associado a uma moeda.

    Atributos:
        valor (int): O valor monetário representando em centavos com inteiros. e.g. R$1,99 = 199
        moeda (Moeda): A moeda na qual o valor é expresso.

    Métodos:
        __init__(valor: int, moeda: Moeda): Inicializa uma instância da classe Preco.
        __repr__(): Retorna uma representação legível do preço.
    """
    def __init__(self, valor: int, moeda: moeda.Moeda):
        if not isinstance(valor, int):
            raise TypeError("O valor deve ser do tipo inteiro.")
        if not isinstance(moeda, moeda.Moeda):
            raise TypeError("A moeda deve ser uma instância da classe Moeda.")

        self.valor = valor
        self.moeda = moeda

    def __repr__(self):
        return f"{self.moeda.simbolo}{self.valor} ({self.moeda.codigo})"

# Exemplo de uso
moeda_brl = moeda.Moeda("BRL", "Real Brasileiro", "R$")
preco = Preco(15000, moeda_brl)
print(preco)  # R$150.75 (BRL)
