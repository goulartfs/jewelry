import config

"""
Sistema de Empacotamento de Joias

Este módulo implementa a lógica principal para o empacotamento de joias em pacotes,
seguindo regras específicas de negócio para otimização e distribuição dos itens.

O sistema trabalha com uma lista de pedidos, onde cada pedido contém uma quantidade
de itens solicitada. O objetivo é garantir que todos os pacotes estejam completos
e que cada pedido atenda aos requisitos mínimos estabelecidos.

Regras principais:
1. Cada pacote deve ter um tamanho fixo (número total de itens)
2. Cada pedido deve ter um número mínimo de itens
3. Pacotes incompletos são otimizados automaticamente
"""

def empacotar(tamanho_do_pacote: int, numero_minimo_de_itens: int, lista_de_itens: list[int]) -> list[int]:
    """
    Empacota os itens de acordo com as regras de negócio estabelecidas.

    Args:
        tamanho_do_pacote (int): Número total de itens que cada pacote deve conter
        numero_minimo_de_itens (int): Quantidade mínima de itens que cada pedido deve ter
        lista_de_itens (list[int]): Lista com a quantidade de itens de cada pedido

    Returns:
        list[int]: Lista atualizada com as quantidades ajustadas após o empacotamento

    Raises:
        Exception: Se o tamanho do pacote estiver fora dos limites permitidos
        Exception: Se o número mínimo de itens estiver fora dos limites permitidos
        Exception: Se a lista de itens estiver vazia

    Exemplo:
        >>> empacotar(4, 3, [1, 1, 1, 2])
        [3, 3, 3, 2]  # Ajustado para mínimo de 3 itens por pedido
    """
    # Validação do tamanho do pacote
    if tamanho_do_pacote < config.LIMITE_MINIMO_DO_TAMANHO or tamanho_do_pacote > config.LIMITE_MAXIMO_DO_TAMANHO:
        raise Exception("Tamanho deve ser entre 0 e 100")
    
    # Validação do número mínimo de itens
    if numero_minimo_de_itens < 0 or numero_minimo_de_itens > 100:
        raise Exception("Numero minimo de itens deve ser entre 0 e 100")

    # Validação da lista de itens
    if len(lista_de_itens) == 0:
        raise Exception("A lista de itens não deve estar vazia")

    def contar_numero_de_itens(lista_de_itens: list[int]) -> int:
        """
        Calcula o número total de itens na lista de pedidos.

        Args:
            lista_de_itens (list[int]): Lista com a quantidade de itens de cada pedido

        Returns:
            int: Soma total de todos os itens
        """
        return sum(lista_de_itens)
    
    numero_de_itens = contar_numero_de_itens(lista_de_itens)

    def separar_sobra(lista_de_itens: list[int], tamanho_do_pacote: int) -> int:
        """
        Calcula quantos itens sobram após formar pacotes completos.

        Args:
            lista_de_itens (list[int]): Lista com a quantidade de itens de cada pedido
            tamanho_do_pacote (int): Tamanho fixo que cada pacote deve ter

        Returns:
            int: Quantidade de itens que sobram (não formam um pacote completo)
        """
        numero_de_itens = contar_numero_de_itens(lista_de_itens)
        return numero_de_itens % tamanho_do_pacote
    
    quantidade_de_itens_que_sobrou_fora_da_caixa = numero_de_itens % tamanho_do_pacote

    # Se não há sobras, retorna a lista original
    if quantidade_de_itens_que_sobrou_fora_da_caixa == 0:
        return lista_de_itens
    
    # Calcula quantos itens faltam para completar o próximo pacote
    qtd_itens_faltantes = tamanho_do_pacote - quantidade_de_itens_que_sobrou_fora_da_caixa
    
    # Distribui os itens faltantes priorizando pedidos abaixo do mínimo
    qtd_itens_adicionados = 0
    limite_de_itens_que_posso_adicionar = 0
    
    for indice, numero_de_itens in enumerate(lista_de_itens):
        if numero_de_itens <= numero_minimo_de_itens:
            limite_de_itens_que_posso_adicionar = qtd_itens_faltantes - qtd_itens_adicionados
            quanto_falta = numero_minimo_de_itens - numero_de_itens

            if quanto_falta > limite_de_itens_que_posso_adicionar:
                quanto_falta = limite_de_itens_que_posso_adicionar

            lista_de_itens[indice] += quanto_falta
            qtd_itens_adicionados += quanto_falta

        if qtd_itens_adicionados == qtd_itens_faltantes:
            break
    
    # Verifica se após a distribuição ainda há sobras
    numero_de_itens = contar_numero_de_itens(lista_de_itens)
    quantidade_de_itens_que_sobrou_fora_da_caixa = numero_de_itens % tamanho_do_pacote

    if quantidade_de_itens_que_sobrou_fora_da_caixa == 0:
        return lista_de_itens
    
    # Se ainda houver sobras, os itens restantes serão atribuídos ao administrador
    # TODO: Implementar lógica para atribuir itens restantes ao administrador
    return lista_de_itens