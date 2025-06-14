# Sistema de Gestão de Joias

Sistema para gestão de joias, incluindo catálogo de produtos, fornecedores, pedidos e clientes.

## Arquitetura

O projeto segue os princípios do Domain-Driven Design (DDD) e Clean Architecture, organizando o código em camadas:

- **Domain**: Contém as regras de negócio e entidades do domínio
  - `shared`: Classes e interfaces base compartilhadas
  - `identity`: Gerenciamento de identidade e acesso
  - `organization`: Gestão da organização e seus membros
  - `catalog`: Catálogo de produtos e fornecedores
  - `order`: Pedidos e transações

- **Application**: Implementa os casos de uso da aplicação
  - Orquestra entidades do domínio
  - Implementa regras de aplicação
  - Define interfaces para infraestrutura

- **Infrastructure**: Implementações concretas
  - Persistência (SQLAlchemy)
  - Mensageria
  - Segurança
  - Logging

- **Presentation**: Interfaces com usuário
  - API REST (FastAPI)
  - CLI

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

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.
