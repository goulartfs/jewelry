import produto

class Documento:
    """
    Representa um documento de identificação.

    Atributos:
        numero (str): O número do documento.
        tipo (str): O tipo do documento (ex: 'CNPJ', 'CPF', 'Passaporte').
    """
    
    def __init__(self, numero: str, tipo: str):
        """
        Inicializa um objeto Documento.

        Parâmetros:
            numero (str): O número do documento.
            tipo (str): O tipo do documento.
        """
        self.numero = numero
        self.tipo = tipo

    def __repr__(self) -> str:
        """
        Retorna uma representação legível do documento.

        Retorna:
            str: String no formato '<tipo>: <numero>'.
        """
        return f"{self.tipo}: {self.numero}"

class Fornecedor:
    """
    Representa um fornecedor que pode ter vários documentos.

    Atributos:
        nome (str): Nome da empresa ou do fornecedor.
        documentos (list): Lista de documentos do fornecedor.
        endereco (str): Endereço do fornecedor.
        produtos (list): Lista de produtos fornecidos pelo fornecedor.
    """

    def __init__(self, 
                 nome: str, 
                 documentos: list[Documento], 
                 endereco: str, 
                 produtos: list[produto.Produto] = None):
        """
        Inicializa uma instância da classe Fornecedor.

        Parâmetros:
            nome (str): Nome do fornecedor.
            documentos (list): Lista de instâncias da classe Documento.
            endereco (str): Endereço do fornecedor.
            produtos (list, opcional): Lista de produtos fornecidos, default é uma lista vazia.
        """
        self.nome = nome
        self.documentos = documentos
        self.endereco = endereco
        self.produtos = produtos if produtos else []  # Inicializa a lista de produtos vazia se nenhum for fornecido.

    def adicionar_produto(self, produto: produto.Produto):
        """
        Adiciona um produto à lista de produtos fornecidos.

        Parâmetros:
            produto (Produto): Instância da classe Produto a ser adicionada.
        """
        self.produtos.append(produto)

    def listar_produtos(self) -> list[produto.Produto]:
        """
        Lista todos os produtos fornecidos.

        Retorna:
            list: Lista de produtos.
        """
        return self.produtos

    def __repr__(self) -> str:
        """
        Retorna uma representação legível do fornecedor.

        Retorna:
            str: String no formato '<nome>: <documentos>'.
        """
        documentos_str = ", ".join([str(doc) for doc in self.documentos])
        return f"{self.nome} - Documentos: [{documentos_str}]"
