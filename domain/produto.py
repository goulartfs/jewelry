import preco

class Produto:
    """
    Representa um produto com SKU, nome, descrição e um preço.

    Atributos:
        sku (str): Código identificador único do produto.
        nome (str): Nome do produto.
        descricao (str): Descrição detalhada do produto.
        preco (Preco): Preço associado ao produto.
    """
    
    def __init__(self, sku: str, nome: str, descricao: str, preco: preco.Preco):
        """
        Inicializa um objeto Produto.

        Parâmetros:
            sku (str): Código identificador único do produto.
            nome (str): Nome do produto.
            descricao (str): Descrição detalhada do produto.
            preco (Preco): Instância da classe Preco representando o preço do produto.
        """
        self.sku = sku
        self.nome = nome
        self.descricao = descricao
        self.preco = preco

    def __repr__(self):
        """
        Retorna uma representação legível do produto.

        Retorna:
            str: String no formato '<nome> (<sku>): <preco>'.
        """
        return f"{self.nome} ({self.sku}): {self.preco}"
