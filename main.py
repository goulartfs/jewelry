"""
Ponto de entrada principal do sistema de empacotamento de joias.

Este módulo demonstra o uso do sistema de empacotamento através de um exemplo
prático, mostrando como configurar os parâmetros e processar uma lista de pedidos.

Exemplo de uso:
    python main.py

O resultado mostrará a lista de pedidos após o processamento, com as quantidades
ajustadas de acordo com as regras de negócio estabelecidas.
"""

import empacotador

# Configuração do tamanho do pacote
# Cada pacote deve conter exatamente esta quantidade de itens
tamanho_do_pacote = 4

# Configuração do número mínimo de itens por pedido
# Cada pedido deve ter pelo menos esta quantidade de itens
numero_minimo_de_itens_por_item_de_pedido = 3

# Lista de pedidos com a quantidade inicial de itens para cada cliente
lista_de_pedido = [
    1,  # maria   - Pedido inicial de 1 item
    1,  # mario   - Pedido inicial de 1 item
    1,  # lucia   - Pedido inicial de 1 item
    2   # ronaldo - Pedido inicial de 2 itens
]

# 5 fecho pacote com 8 - faltam 3, ou seja, preciso de "+3" itens para fechar o pacote

# Processa a lista de pedidos aplicando as regras de empacotamento
resultado = empacotador.empacotar_pedido(
    tamanho=tamanho_do_pacote,
    numero_minimo_de_itens=numero_minimo_de_itens_por_item_de_pedido,
    lista_de_itens=lista_de_pedido
)

# Exibe o resultado do processamento
print(resultado)