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