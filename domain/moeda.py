class Moeda:
    def __init__(self, codigo: str, nome: str, simbolo: str):
        if len(codigo) != 3:
            raise ValueError("O código da moeda deve ser uma string de 3 letras (ex: 'BRL', 'USD').")
        if not nome:
            raise ValueError("O nome da moeda não pode ser vazio.")
        if not simbolo:
            raise ValueError("O símbolo da moeda não pode ser vazio.")

        self.codigo = codigo.upper()  # Ex: 'BRL'
        self.nome = nome              # Ex: 'Real Brasileiro'
        self.simbolo = simbolo        # Ex: 'R$'

    def __repr__(self):
        return f"{self.nome} ({self.codigo}) - {self.simbolo}"

    def __eq__(self, outro):
        return self.codigo == outro.codigo

# Exemplo de uso:
moeda_brl = Moeda("BRL", "Real Brasileiro", "R$")
moeda_usd = Moeda("USD", "Dólar Americano", "$")

print(moeda_brl)  # Real Brasileiro (BRL) - R$
print(moeda_usd)  # Dólar Americano (USD) - $
