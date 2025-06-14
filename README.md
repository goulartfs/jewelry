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
