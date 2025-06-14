# Módulo de Fornecedores

Este documento descreve o módulo de fornecedores do sistema de joias, que é responsável por gerenciar os fornecedores de produtos.

## Entidades

### Fornecedor

A entidade `Fornecedor` representa um fornecedor de produtos no sistema. Ela possui os seguintes atributos:

- `nome`: Nome do fornecedor
- `documentos`: Lista de documentos do fornecedor (CNPJ, CPF, etc.)
- `endereco`: Endereço do fornecedor
- `produtos`: Lista de produtos fornecidos
- `ativo`: Status do fornecedor (ativo/inativo)
- `data_cadastro`: Data de cadastro do fornecedor

### Documento

O objeto de valor `Documento` representa um documento de identificação do fornecedor. Ele possui os seguintes atributos:

- `numero`: Número do documento
- `tipo`: Tipo do documento (CNPJ, CPF, etc.)

## Casos de Uso

### Criar Fornecedor

Permite criar um novo fornecedor no sistema.

**Entrada:**
- Nome do fornecedor
- Documento principal (CNPJ ou CPF)
- Endereço completo

**Regras:**
- O nome não pode estar vazio
- O fornecedor deve ter pelo menos um documento
- Não pode existir outro fornecedor com o mesmo documento
- O documento deve ser válido (CNPJ com 14 dígitos ou CPF com 11 dígitos)
- O endereço deve ser válido e completo

### Atualizar Fornecedor

Permite atualizar os dados de um fornecedor existente.

**Entrada:**
- ID do fornecedor
- Novos dados (nome e/ou endereço)

**Regras:**
- O fornecedor deve existir
- O nome não pode estar vazio
- O endereço deve ser válido e completo

### Adicionar Documento

Permite adicionar um novo documento a um fornecedor.

**Entrada:**
- ID do fornecedor
- Novo documento

**Regras:**
- O fornecedor deve existir
- O documento deve ser válido
- Não pode existir outro fornecedor com o mesmo documento

### Remover Documento

Permite remover um documento de um fornecedor.

**Entrada:**
- ID do fornecedor
- Documento a ser removido

**Regras:**
- O fornecedor deve existir
- O fornecedor deve ter pelo menos um documento após a remoção

### Atualizar Endereço

Permite atualizar o endereço de um fornecedor.

**Entrada:**
- ID do fornecedor
- Novo endereço

**Regras:**
- O fornecedor deve existir
- O endereço deve ser válido e completo

### Desativar Fornecedor

Permite desativar um fornecedor.

**Entrada:**
- ID do fornecedor

**Regras:**
- O fornecedor deve existir

### Ativar Fornecedor

Permite ativar um fornecedor.

**Entrada:**
- ID do fornecedor

**Regras:**
- O fornecedor deve existir

### Buscar por Nome

Permite buscar fornecedores por nome.

**Entrada:**
- Nome ou parte do nome

**Saída:**
- Lista de fornecedores que correspondem à busca

### Listar Fornecedores

Permite listar todos os fornecedores.

**Entrada:**
- Flag para indicar se deve retornar apenas fornecedores ativos

**Saída:**
- Lista de fornecedores

## Arquitetura

O módulo segue a arquitetura limpa (Clean Architecture) com as seguintes camadas:

### Domínio

- `Fornecedor`: Entidade principal
- `Documento`: Objeto de valor
- `FornecedorRepository`: Interface do repositório
- `FornecedorService`: Serviço de domínio

### Aplicação

- `FornecedorAppService`: Serviço de aplicação
- DTOs:
  - `FornecedorDTO`
  - `CriarFornecedorDTO`
  - `AtualizarFornecedorDTO`
  - `ListagemFornecedorDTO`
  - `DocumentoDTO`

### Infraestrutura

- `SQLAlchemyFornecedorRepository`: Implementação do repositório
- Modelos SQLAlchemy:
  - `Fornecedor`
  - `Documento`
- Mapeadores:
  - `FornecedorMapper`

## Testes

O módulo possui testes unitários e de integração para todas as suas funcionalidades:

- `test_fornecedor.py`: Testes da entidade
- `test_documento.py`: Testes do objeto de valor
- `test_fornecedor_service.py`: Testes do serviço de domínio
- `test_fornecedor_app_service.py`: Testes do serviço de aplicação
- `test_fornecedor_repository.py`: Testes do repositório 