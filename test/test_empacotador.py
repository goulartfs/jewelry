import empacotador

def test_1 ():
    tamanho_do_pacote = 10
    lista_pedidos = [1, 3, 3]
    resultado_esperado = [3, 3, 3, 1]
    resultado = empacotador.empacotar(tamanho_do_pacote, 3, lista_pedidos)

    assert resultado == resultado_esperado


def test_2():
    tamanho_do_pacote = 10

    lista_pedidos = [1, 1, 1, 1]
    resultado_esperado = [3, 3, 3, 1]
    resultado = empacotador.empacotar(tamanho_do_pacote, 3, lista_pedidos)

    assert resultado == resultado_esperado


def test_3():
    tamanho_do_pacote = 10

    lista_pedidos = [3, 3, 2, 2]
    resultado_esperado = [3, 3, 2, 2]
    resultado = empacotador.empacotar(tamanho_do_pacote, 3, lista_pedidos)

    assert resultado == resultado_esperado


def test_4():
    tamanho_do_pacote = 10

    lista_pedidos = [3, 3, 2, 2, 3]
    resultado_esperado = [3, 3, 2, 2]
    resultado = empacotador.empacotar(tamanho_do_pacote, 3, lista_pedidos)

    assert resultado == resultado_esperado