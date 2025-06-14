<<<<<<< HEAD
# Sistema de Empacotamento de Joias

Este sistema foi desenvolvido para otimizar o processo de empacotamento de joias, automatizando a estratégia de vendas da Jane Doe, uma lojista que trabalha com acessórios de beleza em atacado para grupos de compra.

## 📝 Contexto do Negócio

Jane Doe é uma lojista que vende acessórios de beleza (anéis, colares, brincos, etc.) em atacado para grupos de compra. Ela trabalha com diversos fornecedores, oferecendo catálogos de produtos aos seus compradores em períodos determinados.

### Sobre o Grupo de Compra

Um grupo de compra é um coletivo de pessoas que desejam comprar produtos a varejo à preço de atacado, onde cada comprador pode optar por um pacote inteiro ou frações dele para cada item desejado.

Por exemplo:
- Um catálogo de anéis com 3 produtos diferentes
- Cada produto é vendido em pacotes de 10 itens
- Preço do pacote: R$ 100,00 (R$ 10,00 por item)

### Processo de Venda

1. Compradores acessam os catálogos
2. Selecionam itens e quantidades desejadas
3. Itens são adicionados à lista de pedido
4. Ao fim do período, os pedidos são processados

## 🎯 Objetivo do Sistema

O sistema automatiza a estratégia de venda da Jane Doe para otimizar o fechamento de pacotes, que consiste em:

1. Editar a quantidade de cada item de pedido até atingir uma quantidade mínima determinada no catálogo
2. Adicionar itens de pedido quando necessário para fechar pacotes

## 🚀 Funcionalidades

- Validação de tamanho de pacotes
- Verificação de quantidade mínima de itens por pedido
- Otimização automática de pacotes incompletos
- Distribuição inteligente de itens adicionais

## 📋 Regras de Negócio

1. **Tamanho do Pacote**
   - Deve ser maior que zero
   - Não pode exceder 100 itens
   - Todos os pacotes devem estar completamente preenchidos

2. **Itens por Pedido**
   - Cada pedido deve ter um número mínimo de itens
   - Se um pedido não atingir o mínimo, será complementado automaticamente

3. **Preenchimento de Pacotes**
   - Pacotes incompletos serão preenchidos seguindo regras específicas
   - Itens adicionais são distribuídos priorizando pedidos abaixo do mínimo
   - Caso necessário, itens restantes são atribuídos ao administrador

## 🛠️ Tecnologias

- Python 3.x
- Pytest para testes unitários

## 📦 Estrutura do Projeto

```
joias/
├── docs/
│   └── diagrama-de-dados.png
├── domain/
├── test/
│   └── test_empacotador.py
├── main.py
├── empacotador.py
└── config.py
```

## 🔧 Como Usar

1. Configure o tamanho do pacote desejado
```python
tamanho_do_pacote = 4
```

2. Defina o número mínimo de itens por pedido
```python
numero_minimo_de_itens_por_item_de_pedido = 3
```

3. Crie sua lista de pedidos
```python
lista_de_pedido = [
    1,  # maria   - Pedido inicial de 1 item
    1,  # mario   - Pedido inicial de 1 item
    1,  # lucia   - Pedido inicial de 1 item
    2   # ronaldo - Pedido inicial de 2 itens
]
```

4. Execute o empacotador
```python
resultado = empacotador.empacotar_pedido(
    tamanho=tamanho_do_pacote,
    numero_minimo_de_itens=numero_minimo_de_itens_por_item_de_pedido,
    lista_de_itens=lista_de_pedido
)
```

## 🧪 Testes

O projeto inclui testes unitários para garantir o funcionamento correto das regras de negócio. Para executar os testes:

```bash
pytest test/test_empacotador.py
```

## 📝 Notas Importantes

- O sistema valida automaticamente os parâmetros de entrada
- Em caso de pacotes incompletos, o sistema tenta otimizar a distribuição
- Todos os ajustes são feitos respeitando as regras de negócio estabelecidas

## 📊 Exemplo Prático de Processamento

### Lista de Pedidos Original
```
Anel Esmeralda:
- Ronaldo: 2 itens
- Janio: 3 itens
- Naldo: 4 itens
- Beatriz: 3 itens
- Emerson: 1 item
- Clara: 4 itens
- Artur: 1 item
Total: 18 itens

Anel Rubi:
- Maria: 1 item
- Leonardo: 2 itens
- Lea: 2 itens
- Artur: 2 itens
- Naldo: 3 itens
Total: 10 itens

Anel Diamante:
- Artur: 3 itens
- Clara: 3 itens
- Daniel: 1 item
- Naldo: 2 itens
Total: 9 itens
```

### Resultado do Processamento
```
Anel Esmeralda:
- 1 Pacote Fechado (10 itens)
- 1 Pacote Aberto (8 itens) -> Sistema otimizará para fechar

Anel Rubi:
- 1 Pacote Fechado (10 itens)

Anel Diamante:
- 1 Pacote Aberto (9 itens) -> Sistema otimizará para fechar
```

O sistema automaticamente ajustará os pedidos para otimizar o fechamento dos pacotes, evitando a perda de vendas em potencial. 
=======
Jane Doe é uma lojista que ganha a vida vendendo acessórios de beleza, bem como anéis, colares, brincos, etc. em atacado para grupos de compra.

Conforme um período determinado, ela oferece aos seus potenciais compradores, catálogos de diferentes fornecedores com os quais ela possui parceria de negócio. 

Seus compradores acessam cada um dos catálogos e conferir todos os itens disponíveis para venda. Dentre a lista de itens disponíveis podem visualizar detalhes de cada item e realizar suas compras. 

Uma vez que o comprador tenha escolhido o item que deseja comprar, deve-se informar os detalhes desejados dentre as opções de cada item e a quantidade desejada. Uma vez preenchido, o item é adicionado a sua lista de pedido.

Dessa forma, Jane Doe realiza centenas de vendas para diversos compradores para diversos catálogos ativos no período em questão.

# Sobre o grupo de compra

Um grupo de compra é um coletivo de pessoas únicas que desejam comprar produtos a varejo à preço de atacado onde cada comprador pode optar por um pacote inteiro ou frações dele para cada item desejado.

Por exemplo: 

imagine que temos um catálogo de anéis,
e que o catálogo possui 3 anéis disponíveis para venda, onde,
cada um dos itens são oferecidos pelo fornecedor
em pacotes compostos por 10 itens, 
onde cada pacote tem o preço total de R$ 100,00 (cem reais).
Ou seja, cada item possui valor unitário de R$ 10,00 (dez reais).

Catálogo: 

    1. Anéis Bafônicos
    
Items:

    1. Anel Esmeralda
    2. Anel Diamante
    3. Anel Rubi
    
Lista de Pedido:

    #. Comprador  - Item de Pedido - Qtd     - R$
    ---------------------------------------------------
    1. Ronaldo    - Anel Esmeralda - 2 itens - R$ 20,00
    2. Maria      - Anel Rubi      - 1 item  - R$ 10,00
    3. Janio      - Anel Esmeralda - 3 itens - R$ 30,00
    4. Artur      - Anel Diamante  - 3 itens - R$ 30,00
    5. Clara      - Anel Diamante  - 3 itens - R$ 30,00
    6. Leonardo   - Anel Rubi      - 2 itens - R$ 20,00
    7. Naldo      - Anel Esmeralda - 4 itens - R$ 40,00
    8. Lea        - Anel Rubi      - 2 itens - R$ 20,00
    9. Beatriz    - Anel Esmeralda - 3 itens - R$ 30,00
    10. Daniel    - Anel Diamante  - 1 item  - R$ 10,00
    11. Emerson   - Anel Esmeralda - 1 item  - R$ 10,00
    12. Artur     - Anel Rubi      - 2 itens - R$ 20,00
    13. Clara     - Anel Esmeralda - 4 itens - R$ 40,00
    14. Naldo     - Anel Diamante  - 2 itens - R$ 20,00
    15. Naldo     - Anel Rubi      - 3 itens - R$ 30,00
    16. Artur     - Anel Esmeralda - 1 item  - R$ 10,00

Ao fim do período de venda, para cada item disponível, 
será verificado se o total de itens pedidos é suficientes para fechar a compra de todo o pacote.

Dada a lista de pedido detalhada anteriormente, devemos sumarizar os itens

Lista de Pedidos Sumarizada:

-----------------------------------------------
Anel Esmeralda
-----------------------------------------------
    01. Ronaldo   - Anel Esmeralda - 2 itens - R$ 20,00
    03. Janio     - Anel Esmeralda - 3 itens - R$ 30,00
    07. Naldo     - Anel Esmeralda - 4 itens - R$ 40,00
    09. Beatriz   - Anel Esmeralda - 3 itens - R$ 30,00
    11. Emerson   - Anel Esmeralda - 1 item  - R$ 10,00
    13. Clara     - Anel Esmeralda - 4 itens - R$ 40,00
    16. Artur     - Anel Esmeralda - 1 item  - R$ 10,00
-----------------------------------------------
Total de 18 items
-----------------------------------------------

-----------------------------------------------
Anel Rubi
-----------------------------------------------
    02. Maria     - Anel Rubi      - 1 item  - R$ 10,00
    06. Leonardo  - Anel Rubi      - 2 itens - R$ 20,00
    08. Lea       - Anel Rubi      - 2 itens - R$ 20,00
    12. Artur     - Anel Rubi      - 2 itens - R$ 20,00
    15. Naldo     - Anel Rubi      - 3 itens - R$ 30,00
-----------------------------------------------
Total de 10 items
-----------------------------------------------

-----------------------------------------------
Anel Diamante
-----------------------------------------------
    04. Artur     - Anel Diamante  - 3 itens - R$ 30,00
    05. Clara     - Anel Diamante  - 3 itens - R$ 30,00
    10. Daniel    - Anel Diamante  - 1 item  - R$ 10,00
    14. Naldo     - Anel Diamante  - 2 itens - R$ 20,00
-----------------------------------------------
Total de 9 items
-----------------------------------------------

Assim sendo, para cada produto temos:

    01. Anel Esmeralda - 18 itens - R$ 180,00
    02. Anel Rubi      - 10 itens - R$ 100,00
    03. Anel Diamante  - 09 itens - R$  90,00

Conforme definido pela negociação com o fornecedor, 
cada produto é vendido em pacotes com 10 itens.

Sendo assim, teremos:

Para, "01. Anel Esmeralda - 18 itens", temos:
    1. Pacote Fechado (10 itens)
    1. Pacote Aberto  (08 itens)

Para, "02. Anel Rubi      - 10 itens", temos:
    1. Pacote Fechado (10 itens)

Para, "03. Anel Diamante  - 09 itens", temos:
    1. Pacote Aberto  (09 itens)

Neste etapa do processo, sem que haja edição por parte da Jane Doe, 
seria possivel concretizar a venda de apenas 2 pacotes de item, 
descartando a venda de outros 2 pacotes em potencial. 

Em valores monetários, deixariamos de lado o faturamento de R$ 170,00.

Para que essa venda em potencial não seja descartada, Jane Doe criou uma estratégia de venda.
A estratégia de venda consiste em:

1. Editar a lista de pedidos, editando a quantidade de cada item de pedido até que atinja uma determinada quantidade mínima (determinada no catálogo)
2. Editar a lista de pedidos, adicionando um item de pedido definindo a quantidade com o valor minimo necessário para que o pacote seja fechado



# Sobre o produto que está a venda

Como a Jane Doe possui fornecedores distintos, cada um possui uma forma de negociação. 

# Sobre a lista de pedido

Para cada catálogo que a Jane Doe possui, associado ao catálogo existe uma lista de pedido. Essa lista de pedido é preenchida ao longo do período por cada um dos compradores da Jane Doe com detalhes de cada item desejado bem como suas quantidades.

Quando o período de venda do catálogo termina, a lista de pedidos é fechada para faturamento, empacotamento e expedição.

Quando a lista de pedidos é fechada, manualmente a Jane Doe contabiliza cada item buscando fechar cada pacote de item.

>>>>>>> 3ce034e9156eeb86ae87e1b5781d2795c998f7da
