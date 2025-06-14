# Sistema de Gestão de Joias

Sistema para gestão de joias, incluindo catálogo de produtos, fornecedores, pedidos e clientes.

## Visão Geral do Negócio

### Empacotamento de Joias

O sistema gerencia o empacotamento eficiente de joias em caixas, seguindo regras específicas:

1. **Regras de Empacotamento**:
   - Cada joia tem um valor específico ($)
   - Cada caixa tem um limite de peso (gramas)
   - O objetivo é maximizar o valor total em cada caixa
   - Joias mais valiosas têm prioridade no empacotamento

2. **Processo de Empacotamento**:
   ```
   Entrada: [peso valor]
   50 100    # Joia de 50g valendo $100
   30 45     # Joia de 30g valendo $45
   20 30     # Joia de 20g valendo $30
   
   Limite da Caixa: 80g
   
   Saída: [índice]
   1,3    # Joias #1 e #3 totalizam 70g e $130
   2      # Joia #2 sozinha (30g, $45)
   ```

3. **Benefícios**:
   - Otimização do espaço de transporte
   - Maximização do valor por remessa
   - Redução de custos logísticos
   - Rastreabilidade das joias

## Arquitetura

O projeto segue os princípios do Domain-Driven Design (DDD) e Clean Architecture, organizando o código em camadas:

### Domain Layer

Contém as regras de negócio e entidades do domínio:

- **shared/**: Classes e interfaces base compartilhadas
  - `AggregateRoot`: Base para agregados do domínio
  - `DomainEvent`: Base para eventos do domínio
  - `ValueObject`: Base para objetos de valor
  - `Email`: Implementação de e-mail como objeto de valor

- **identity/**: Gerenciamento de identidade e acesso
  - Autenticação e autorização
  - Perfis de usuário
  - Controle de acesso

- **catalog/**: Catálogo de produtos e fornecedores
  - Gestão de joias
  - Cadastro de fornecedores
  - Precificação
  - Categorização

- **order/**: Pedidos e transações
  - Processamento de pedidos
  - Empacotamento de joias
  - Rastreamento de envios
  - Faturamento

### Application Layer

Implementa os casos de uso da aplicação:

- Orquestra entidades do domínio
- Implementa regras de aplicação
- Define interfaces para infraestrutura
- Gerencia transações
- Coordena eventos do domínio

### Infrastructure Layer

Implementações concretas:

- **Persistência**:
  - SQLAlchemy para ORM
  - Migrations com Alembic
  - Repositórios concretos

- **Mensageria**:
  - Eventos assíncronos
  - Filas de processamento
  - Notificações

- **Segurança**:
  - Autenticação JWT
  - Criptografia
  - Auditoria

- **Logging**:
  - Rastreamento de operações
  - Monitoramento
  - Diagnóstico

### Presentation Layer

Interfaces com usuário:

- **API REST** (FastAPI):
  - Documentação OpenAPI
  - Validação de entrada
  - Serialização de dados
  - Tratamento de erros

- **CLI**:
  - Operações em lote
  - Scripts de manutenção
  - Ferramentas de diagnóstico

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/fsynthis/joias.git
cd joias
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite .env com suas configurações
```

5. Execute as migrações:
```bash
alembic upgrade head
```

## Desenvolvimento

1. Instale as dependências de desenvolvimento:
```bash
pip install -r requirements.txt
```

2. Execute os testes:
```bash
pytest
```

3. Verifique a cobertura de testes:
```bash
pytest --cov=src/joias
```

4. Execute o linter:
```bash
flake8 src tests
```

5. Execute o verificador de tipos:
```bash
mypy src tests
```

## Executando

1. Inicie o servidor de desenvolvimento:
```bash
uvicorn src.joias.presentation.api.main:app --reload
```

2. Acesse a documentação da API:
```
http://localhost:8000/docs
```

## Docker

O projeto inclui configuração para Docker:

1. Construa a imagem:
```bash
docker build -t joias .
```

2. Execute o container:
```bash
docker-compose up -d
```

## Estrutura do Projeto

```
src/joias/
├── application/        # Casos de uso e serviços
├── domain/            # Regras e entidades de negócio
│   ├── shared/        # Componentes compartilhados
│   ├── identity/      # Gestão de identidade
│   ├── catalog/       # Catálogo de produtos
│   └── order/         # Gestão de pedidos
├── infrastructure/    # Implementações técnicas
└── presentation/      # Interfaces de usuário
```

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Faça commit das alterações (`git commit -am 'Adiciona nova feature'`)
4. Faça push para a branch (`git push origin feature/nova-feature`)
5. Crie um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

### US2: Visualização de Usuário

Endpoint para consultar os detalhes de um usuário específico:

```http
GET /api/usuarios/{id}
```

**Respostas:**
- `200 OK`: Usuário encontrado
  ```json
  {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "nome": "João da Silva",
      "email": "joao@email.com",
      "ativo": true,
      "data_criacao": "2023-11-21T10:30:00Z"
  }
  ```
- `404 Not Found`: Usuário não encontrado
  ```json
  {
      "erro": "Usuário não encontrado"
  }
  ```

### US3: Listagem de Usuários

Endpoint para listar usuários com paginação e filtros:

```http
GET /api/usuarios?pagina=1&tamanho=10&nome=João&email=joao@email.com
```

**Parâmetros:**
- `pagina`: Número da página (padrão: 1)
- `tamanho`: Quantidade de itens por página (padrão: 10)
- `nome`: Filtro por nome (opcional)
- `email`: Filtro por email (opcional)

**Respostas:**
- `200 OK`: Lista de usuários
  ```json
  [
      {
          "id": "123e4567-e89b-12d3-a456-426614174000",
          "nome": "João da Silva",
          "email": "joao@email.com",
          "ativo": true,
          "data_criacao": "2023-11-21T10:30:00Z"
      }
  ]
  ```

### US4: Atualização de Usuário

Endpoint para atualizar os dados de um usuário existente:

```http
PUT /api/usuarios/{id}
```

**Corpo da Requisição:**
```json
{
    "nome": "João Silva",
    "email": "joao.silva@email.com",
    "ativo": true
}
```

**Observações:**
- Todos os campos são opcionais
- Apenas os campos fornecidos serão atualizados
- O email deve ser único no sistema
- A senha não pode ser alterada por este endpoint

**Respostas:**
- `200 OK`: Usuário atualizado
  ```json
  {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "nome": "João Silva",
      "email": "joao.silva@email.com",
      "ativo": true,
      "data_criacao": "2023-11-21T10:30:00Z"
  }
  ```
- `404 Not Found`: Usuário não encontrado
  ```json
  {
      "erro": "Usuário não encontrado"
  }
  ```
- `409 Conflict`: Email já cadastrado
  ```json
  {
      "erro": "Email já cadastrado"
  }
  ```
- `400 Bad Request`: Dados inválidos
  ```json
  {
      "erro": "Nome não pode ser vazio"
  }
  ```

### US5: Exclusão de Usuário

Endpoint para excluir um usuário do sistema:

```http
DELETE /api/usuarios/{id}
```

**Observações:**
- A exclusão é permanente e não pode ser desfeita
- Não é possível excluir um usuário que possui pedidos ativos
- Requer autenticação e permissões adequadas

**Respostas:**
- `204 No Content`: Usuário excluído com sucesso
- `404 Not Found`: Usuário não encontrado
  ```json
  {
      "erro": "Usuário não encontrado"
  }
  ```
- `409 Conflict`: Usuário possui dependências
  ```json
  {
      "erro": "Usuário possui pedidos ativos"
  }
  ```

### US6: Autenticação e Autorização

O sistema implementa um mecanismo robusto de autenticação e autorização baseado em perfis de usuário.

#### Endpoints de Autenticação

1. **Login**
```http
POST /api/auth/login
```

**Requisição:**
```json
{
    "email": "usuario@email.com",
    "senha": "senha123"
}
```

**Respostas:**
- `200 OK`: Login bem-sucedido
  ```json
  {
      "access_token": "eyJhbGciOiJIUzI1NiIs...",
      "token_type": "bearer",
      "expires_in": 3600
  }
  ```
- `401 Unauthorized`: Credenciais inválidas
  ```json
  {
      "erro": "Email ou senha inválidos"
  }
  ```

#### Endpoints de Perfil

1. **Criar Perfil**
```http
POST /api/perfis
```

**Requisição:**
```json
{
    "nome": "Administrador",
    "descricao": "Acesso total ao sistema",
    "permissoes": ["criar_usuario", "editar_usuario", "excluir_usuario"]
}
```

**Respostas:**
- `201 Created`: Perfil criado
  ```json
  {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "nome": "Administrador",
      "descricao": "Acesso total ao sistema",
      "permissoes": ["criar_usuario", "editar_usuario", "excluir_usuario"],
      "data_criacao": "2024-03-19T14:30:00Z"
  }
  ```

2. **Listar Perfis**
```http
GET /api/perfis
```

**Respostas:**
- `200 OK`: Lista de perfis
  ```json
  {
      "perfis": [
          {
              "id": "123e4567-e89b-12d3-a456-426614174000",
              "nome": "Administrador",
              "descricao": "Acesso total ao sistema",
              "permissoes": ["criar_usuario", "editar_usuario", "excluir_usuario"]
          },
          {
              "id": "987fcdeb-a654-3210-9876-543210987654",
              "nome": "Vendedor",
              "descricao": "Acesso às funcionalidades de vendas",
              "permissoes": ["visualizar_catalogo", "criar_pedido"]
          }
      ]
  }
  ```

3. **Atribuir Perfil a Usuário**
```http
POST /api/usuarios/{usuario_id}/perfis
```

**Requisição:**
```json
{
    "perfil_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

**Respostas:**
- `200 OK`: Perfil atribuído com sucesso
  ```json
  {
      "mensagem": "Perfil atribuído com sucesso"
  }
  ```
- `404 Not Found`: Usuário ou perfil não encontrado
  ```json
  {
      "erro": "Usuário ou perfil não encontrado"
  }
  ```

#### Autorização em Endpoints

Todos os endpoints protegidos devem incluir o token JWT no header:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

O sistema verifica automaticamente:
1. Validade do token
2. Permissões do usuário
3. Escopo do acesso

Em caso de acesso não autorizado:
- `401 Unauthorized`: Token inválido ou expirado
- `403 Forbidden`: Usuário sem permissão necessária

### US7: Cadastro e Associação de Permissões

Endpoints para gerenciamento de permissões e sua associação com perfis.

#### Endpoints de Permissão

1. **Criar Permissão**
```http
POST /permissoes
```

**Requisição:**
```json
{
    "nome": "Acesso Total",
    "chave": "ACCESS_ALL",
    "descricao": "Permite acesso total ao sistema"
}
```

**Respostas:**
- `201 Created`: Permissão criada
  ```json
  {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "nome": "Acesso Total",
      "chave": "ACCESS_ALL",
      "descricao": "Permite acesso total ao sistema"
  }
  ```
- `400 Bad Request`: Dados inválidos
  ```json
  {
      "detail": "Chave de permissão já cadastrada: ACCESS_ALL"
  }
  ```

2. **Buscar Permissão**
```http
GET /permissoes/{id}
```

**Respostas:**
- `200 OK`: Permissão encontrada
  ```json
  {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "nome": "Acesso Total",
      "chave": "ACCESS_ALL",
      "descricao": "Permite acesso total ao sistema"
  }
  ```
- `404 Not Found`: Permissão não encontrada
  ```json
  {
      "detail": "Permissão não encontrada"
  }
  ```

3. **Listar Permissões**
```http
GET /permissoes
```

**Resposta:**
```json
[
    {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "nome": "Acesso Total",
        "chave": "ACCESS_ALL",
        "descricao": "Permite acesso total ao sistema"
    },
    {
        "id": "223e4567-e89b-12d3-a456-426614174000",
        "nome": "Leitura de Pedidos",
        "chave": "READ_ORDERS",
        "descricao": "Permite visualizar pedidos"
    }
]
```

#### Endpoints de Associação Perfil-Permissão

1. **Adicionar Permissão ao Perfil**
```http
POST /perfis/{perfil_id}/permissoes/{permissao_id}
```

**Respostas:**
- `200 OK`: Permissão adicionada
  ```json
  {
      "id": "323e4567-e89b-12d3-a456-426614174000",
      "nome": "Administrador",
      "descricao": "Perfil com acesso total",
      "data_criacao": "2024-01-20T10:30:00Z",
      "permissoes": [
          {
              "id": "123e4567-e89b-12d3-a456-426614174000",
              "nome": "Acesso Total",
              "chave": "ACCESS_ALL",
              "descricao": "Permite acesso total ao sistema"
          }
      ]
  }
  ```
- `404 Not Found`: Perfil ou permissão não encontrados
  ```json
  {
      "detail": "Perfil não encontrado"
  }
  ```

2. **Remover Permissão do Perfil**
```http
DELETE /perfis/{perfil_id}/permissoes/{permissao_id}
```

**Respostas:**
- `200 OK`: Permissão removida
  ```json
  {
      "id": "323e4567-e89b-12d3-a456-426614174000",
      "nome": "Administrador",
      "descricao": "Perfil com acesso total",
      "data_criacao": "2024-01-20T10:30:00Z",
      "permissoes": []
  }
  ```
- `404 Not Found`: Perfil ou permissão não encontrados
  ```json
  {
      "detail": "Permissão não encontrada"
  }
  ```

#### Observações

1. A chave da permissão (`chave`) é única e usada no código para verificação de acesso
2. A chave é automaticamente convertida para maiúsculas ao ser salva
3. Um perfil pode ter múltiplas permissões
4. Uma permissão pode estar associada a múltiplos perfis
5. A remoção de uma permissão de um perfil não exclui a permissão do sistema

### US8: Visualização de Perfil

Endpoint para consultar os detalhes de um perfil específico.

```http
GET /perfis/{id}
```

**Respostas:**
- `200 OK`: Perfil encontrado
  ```json
  {
      "id": "323e4567-e89b-12d3-a456-426614174000",
      "nome": "Administrador",
      "descricao": "Perfil com acesso total",
      "data_criacao": "2024-01-20T10:30:00Z",
      "permissoes": [
          {
              "id": "123e4567-e89b-12d3-a456-426614174000",
              "nome": "Acesso Total",
              "chave": "ACCESS_ALL",
              "descricao": "Permite acesso total ao sistema"
          }
      ]
  }
  ```
- `404 Not Found`: Perfil não encontrado
  ```json
  {
      "detail": "Perfil não encontrado"
  }
  ```

#### Observações

1. O endpoint retorna todos os detalhes do perfil, incluindo suas permissões associadas
2. A resposta inclui a data de criação do perfil
3. As permissões são retornadas com todos os seus detalhes (id, nome, chave e descrição)
4. O acesso a este endpoint requer autenticação
5. A remoção de uma permissão de um perfil não exclui a permissão do sistema

### US9: Atualização de Perfil

Endpoint para atualizar os dados de um perfil existente.

```http
PUT /perfis/{id}
```

**Requisição:**
```json
{
    "nome": "Administrador Sênior",
    "descricao": "Perfil com acesso total ao sistema"
}
```

**Observações:**
- Todos os campos são opcionais
- Apenas os campos fornecidos serão atualizados
- O nome deve ser único no sistema
- As permissões não são alteradas por este endpoint

**Respostas:**
- `200 OK`: Perfil atualizado
  ```json
  {
      "id": "323e4567-e89b-12d3-a456-426614174000",
      "nome": "Administrador Sênior",
      "descricao": "Perfil com acesso total ao sistema",
      "data_criacao": "2024-01-20T10:30:00Z",
      "permissoes": [
          {
              "id": "123e4567-e89b-12d3-a456-426614174000",
              "nome": "Acesso Total",
              "chave": "ACCESS_ALL",
              "descricao": "Permite acesso total ao sistema"
          }
      ]
  }
  ```
- `404 Not Found`: Perfil não encontrado
  ```json
  {
      "detail": "Perfil não encontrado"
  }
  ```
- `400 Bad Request`: Nome já cadastrado
  ```json
  {
      "detail": "Nome de perfil já cadastrado: Administrador Sênior"
  }
  ```

### US10: Exclusão de Perfil

Endpoint para excluir um perfil do sistema.

```http
DELETE /perfis/{id}
```

**Observações:**
- A exclusão é permanente e não pode ser desfeita
- Não é possível excluir um perfil que possui permissões associadas
- É necessário remover todas as permissões do perfil antes de excluí-lo
- Requer autenticação e permissões adequadas

**Respostas:**
- `204 No Content`: Perfil excluído com sucesso
- `404 Not Found`: Perfil não encontrado
  ```json
  {
      "detail": "Perfil não encontrado"
  }
  ```
- `409 Conflict`: Perfil possui permissões associadas
  ```json
  {
      "detail": "Não é possível excluir um perfil que possui permissões associadas"
  }
  ```

### US11: Criação de Permissão

Endpoint para criar uma nova permissão no sistema.

```http
POST /permissoes
```

**Requisição:**
```json
{
    "nome": "Acesso Total",
    "chave": "ACCESS_ALL",
    "descricao": "Permite acesso total ao sistema"
}
```

**Observações:**
- Todos os campos são obrigatórios
- A chave é automaticamente convertida para maiúsculas
- A chave deve ser única no sistema
- A chave é utilizada no código para verificação de acesso
- Requer autenticação e permissões adequadas

**Respostas:**
- `201 Created`: Permissão criada
  ```json
  {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "nome": "Acesso Total",
      "chave": "ACCESS_ALL",
      "descricao": "Permite acesso total ao sistema"
  }
  ```
- `400 Bad Request`: Dados inválidos ou chave já existente
  ```json
  {
      "detail": "Chave de permissão já cadastrada: ACCESS_ALL"
  }
  ```
