import fornecedor
import produto

class Catalogo:
    fornecedor: fornecedor.Fornecedor
    produtos: list[produto.Produto]
    link: string