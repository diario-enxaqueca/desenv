# Diário de Enxaqueca - Desenvolvimento

Sistema completo de gerenciamento de crises de enxaqueca desenvolvido, incluindo backend FastAPI, autenticação JWT, frontend React e testes automatizados.

## Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Tecnologias](#tecnologias)
- [Arquitetura](#arquitetura)
- [Pré-requisitos](#pré-requisitos)
- [Instalação e Execução](#instalação-e-execução)
- [Scripts de Automação](#scripts-de-automação)
- [Testes](#testes)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Documentação](#documentação)
- [Contribuição](#contribuição)

## Sobre o Projeto

O Diário de Enxaqueca é uma aplicação web desenvolvida para ajudar pessoas que sofrem com enxaqueca a registrar e monitorar suas crises, identificar gatilhos e gerenciar medicações. O projeto foi desenvolvido como trabalho da disciplina de Técnicas de Programação para Plataformas Emergentes (TPPE) da FGA/UnB.

### Funcionalidades

- **Autenticação e Autorização**: Sistema completo de registro, login e gerenciamento de usuários
- **Registro de Episódios**: Documentação detalhada de crises de enxaqueca (data, duração, intensidade, sintomas)
- **Gatilhos**: Identificação e categorização de fatores desencadeantes
- **Medicações**: Gerenciamento de medicamentos utilizados e sua eficácia
- **Dashboard**: Visualização de dados e padrões das crises

## Tecnologias

### Backend
- **Python 3.11.14**
- **FastAPI** - Framework web moderno e de alta performance
- **SQLAlchemy** - ORM para manipulação do banco de dados
- **Pydantic V2** - Validação de dados e serialização
- **JWT** - Autenticação baseada em tokens
- **pytest** - Framework de testes (cobertura de 95%)
- **Pylint** - Análise estática de código (nota 9.60/10)

### Frontend
- **React** - Biblioteca para construção de interfaces
- **Vite** - Build tool e dev server
- **TypeScript** - Superset tipado do JavaScript
- **Tailwind CSS** - Framework CSS utilitário

### Infraestrutura
- **Docker & Docker Compose** - Containerização e orquestração
- **MySQL 8** - Banco de dados relacional
  - Desenvolvimento: MySQL local (Docker)
  - Produção: Aiven Cloud (mysql-2e80f044-diario-de-enxaqueca.k.aivencloud.com)
- **Nginx** - Servidor web para o frontend

### Testes
- **pytest** - Testes unitários e de integração (Python)
- **Selenium** - Testes end-to-end automatizados

## Arquitetura

O projeto utiliza uma **arquitetura MVC (Model-View-Controller)** modular, com estrutura de pastas preparada para futura migração para microsserviços. Cada módulo (episódio, gatilho, medicação, usuário) possui separação clara de responsabilidades seguindo o padrão MVC, facilitando a extração para serviços independentes quando necessário.

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Frontend  │─────▶│   Backend    │─────▶│    MySQL    │
│  (React)    │      │  (FastAPI)   │      │  Database   │
└─────────────┘      │   MVC API    │      └─────────────┘
                     └──────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │     Auth     │
                     │   Module     │
                     └──────────────┘
```

### Componentes

- **frontend**: Interface do usuário (porta 3000)
- **backend**: API principal seguindo padrão MVC (porta 8000)
  - Módulos: episodio, gatilho, medicacao, usuario
  - Cada módulo possui: Model, View (rotas), Controller, Schemas
- **autenticacao**: Módulo de autenticação separado (porta 8001)
- **db**: Banco de dados MySQL
  - Local: MySQL Docker (porta 3306)
  - Produção: Aiven Cloud MySQL (porta 24445, SSL obrigatório)
- **tests**: Ambiente para testes unitários
- **tests-auth**: Ambiente para testes de autenticação
- **lint**: Análise estática de código
- **selenium**: Testes end-to-end automatizados

## Pré-requisitos

Para executar o projeto localmente, você precisa ter instalado:

- **Docker Desktop** (ou Docker Engine + Docker Compose)
  - Windows/Mac: [Docker Desktop](https://www.docker.com/products/docker-desktop)
  - Linux: [Docker Engine](https://docs.docker.com/engine/install/)
- **Git** para clonar o repositório

### Opcional (para desenvolvimento)
- **Node.js 18+** (desenvolvimento frontend)
- **Python 3.11+** (desenvolvimento backend)

## Instalação e Execução

### 1. Clonar o Repositório

```bash
git clone https://github.com/diario-enxaqueca/desenvolvimento.git
cd desenvolvimento
```

### 2. Configurar Variáveis de Ambiente

O projeto já possui um arquivo `.env` pré-configurado para desenvolvimento local. Caso precise ajustar, edite o arquivo `.env` na raiz do projeto.

**Principais variáveis:**
```env
MYSQL_ROOT_PASSWORD=root_password
MYSQL_USER=diario_user
MYSQL_PASSWORD=diario_password
MYSQL_DB=diario_enxaqueca
MYSQL_HOST=db
SECRET_KEY=your-secret-key-here
```

### 3. Executar o Projeto

#### Opção 1: Subir todos os serviços

```bash
docker-compose up --build -d
```

Este comando irá:
- Construir todas as imagens Docker
- Criar e iniciar todos os containers
- Configurar a rede interna entre os serviços
- Executar as migrations do banco de dados

#### Opção 2: Subir serviços específicos

```bash
# Apenas backend e banco de dados
docker-compose up db backend auth -d

# Incluir frontend
docker-compose up db backend auth frontend -d
```

### 4. Verificar Status dos Serviços

```bash
# Ver status de todos os containers
docker-compose ps

# Ver logs em tempo real
docker-compose logs -f

# Ver logs de um serviço específico
docker-compose logs -f backend
```

### 5. Acessar a Aplicação

Após todos os serviços estarem rodando (aguarde 30-60 segundos para inicialização completa):

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Backend Docs**: http://localhost:8000/docs (Swagger UI)
- **Auth Service**: http://localhost:8001
- **Auth Docs**: http://localhost:8001/docs

### 6. Parar os Serviços

```bash
# Parar todos os containers
docker-compose down

# Parar e remover volumes (limpa banco de dados)
docker-compose down -v
```

## Scripts de Automação

O projeto disponibiliza scripts PowerShell na pasta `scripts/` para facilitar operações comuns durante o desenvolvimento:

### capture-logs.ps1

Captura logs de todos os serviços em execução e salva em arquivos separados na pasta `logs/`.

```powershell
.\scripts\capture-logs.ps1
```

**Logs gerados:**
- `logs/backend.log` - Logs do serviço backend
- `logs/auth.log` - Logs do serviço de autenticação
- `logs/frontend.log` - Logs do frontend
- `logs/tests.log` - Saída dos testes unitários e de integração do backend
- `logs/tests.log` - Saída dos testes unitários e de integraçãode autenticação
- `logs/lint.log` - Resultado da análise de código

### stop-logs.ps1

Para a captura de logs dos serviços Docker em execução de forma segura.

```powershell
.\scripts\stop-logs.ps1
```

### stop-then-capture-logs-com-build-no-cache.ps1

Script completo que:
1. Para todos os serviços
2. Reconstrói as imagens sem cache (`--no-cache`)
3. Inicia todos os serviços
4. Executa todos os testes (unitários, integração, lint, Selenium)
5. Inicia a captura todos os logs

```powershell
.\scripts\stop-then-capture-logs-com-build-no-cache.ps1
```

**Uso recomendado:**
- Use este script para validação completa antes de commits importantes
- Útil para garantir que o build está limpo e todos os testes passam
- Gera um conjunto completo de logs para debug

## Testes

O projeto possui cobertura de **95%** de testes com diferentes níveis de teste.

### Testes Unitários e de Integração

```bash
# Executar todos os testes do backend
docker-compose run --rm tests

# Executar testes do serviço de autenticação
docker-compose run --rm tests-auth

# Executar testes com cobertura
docker-compose run --rm tests pytest --cov=source --cov-report=html

# Ver relatório de cobertura
# Abra backend/htmlcov/index.html no navegador
```

### Testes de Lint

```bash
# Executar análise de código
docker-compose run --rm lint pylint --rcfile=.pylintrc backend/source/*/*.py

# Executar lint completo
docker-compose run --rm lint
```

### Testes End-to-End (Selenium)

```bash
# Executar testes Selenium
docker-compose run --rm selenium

# Executar teste específico
docker-compose run --rm selenium pytest frontend/tests-selenium/test_diariodeenxaquecaCRUDusuario.py
```

## Estrutura do Projeto

```
desenvolvimento/
├── autenticacao/              # Serviço de autenticação
│   ├── auth/                  # Lógica de autenticação
│   │   ├── controller_auth.py # Lógica de negócio
│   │   ├── model_auth.py      # Modelo de dados
│   │   ├── schemas_auth.py    # Schemas Pydantic
│   │   ├── view_auth.py       # Rotas da API
│   │   └── test_auth.py       # Testes
│   ├── config/                # Configurações
│   └── htmlcov/               # Relatório de cobertura
│
├── backend/                   # API principal
│   ├── config/                # Configurações do banco
│   ├── mysql-init/            # Scripts de inicialização do DB
│   ├── source/                # Código fonte
│   │   ├── episodio/          # CRUD de episódios
│   │   ├── gatilho/           # CRUD de gatilhos
│   │   ├── medicacao/         # CRUD de medicações
│   │   └── usuario/           # CRUD de usuários
│   ├── htmlcov/               # Relatório de cobertura
│   ├── main.py                # Ponto de entrada da API
│   └── requirements.txt       # Dependências Python
│
├── frontend/                  # Interface React
│   ├── src/                   # Código fonte React
│   ├── tests-selenium/        # Testes E2E
│   ├── build/                 # Build de produção
│   └── package.json           # Dependências Node
│
├── documentacao/              # Documentação do projeto
│   ├── docs/                  # Documentos Markdown
│   └── assets/                # Imagens e recursos
│
├── logs/                      # Logs de execução
├── scripts/                   # Scripts de automação
│
├── docker-compose.yml         # Orquestração dos serviços
├── Dockerfile                 # Build do backend
├── Dockerfile.selenium        # Build dos testes E2E
├── .pylintrc                  # Configuração do Pylint
├── .env                       # Variáveis de ambiente
└── README.md                  # Este arquivo
```

### Organização dos Módulos

Cada módulo do backend (episodio, gatilho, medicacao, usuario) segue o padrão MVC:

- **model_*.py**: Modelos SQLAlchemy (entidades do banco)
- **schemas_*.py**: Schemas Pydantic (validação e serialização)
- **controller_*.py**: Lógica de negócio
- **view_*.py**: Rotas da API (endpoints FastAPI)
- **test_*.py**: Testes unitários
- **test_integration_*.py**: Testes de integração

## Qualidade do Código

### Métricas

- **Cobertura de Testes**: 95%
- **Pylint Score**: 9.60/10
- **Testes Passing**: 34/34 (100%)
- **Pydantic**: V2 (latest)
- **Python**: 3.11.14

### Boas Práticas Implementadas

- Validação de dados com Pydantic V2
- Testes unitários e de integração
- Análise estática de código
- Containerização completa
- Separação de responsabilidades (MVC)
- Autenticação JWT
- Documentação automática (Swagger/OpenAPI)

## Documentação

### Documentação da API

Acesse a documentação interativa Swagger UI:
- Backend: http://localhost:8000/docs
- Auth: http://localhost:8001/docs

### Documentação do Projeto

Consulte a pasta `documentacao/` para:
- Backlog e histórias de usuário
- Regras de negócio
- Guia de estilo e protótipo Figma
- DDL e modelo físico do banco de dados
- Guias de contribuição

## Contribuição

### Workflow de Desenvolvimento

1. **Fork** o projeto
2. **Clone** seu fork
3. Crie uma **branch** para sua feature (`git checkout -b feature/MinhaFeature`)
4. **Desenvolva** sua feature
5. **Teste** suas alterações (`docker-compose run --rm tests`)
6. **Lint** seu código (`docker-compose run --rm lint`)
7. **Commit** suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
8. **Push** para a branch (`git push origin feature/MinhaFeature`)
9. Abra um **Pull Request**

### Padrões de Código

- Seguir PEP 8 para código Python
- Manter cobertura de testes acima de 90%
- Passar em todos os testes antes de fazer PR
- Adicionar testes para novas funcionalidades
- Documentar funções e classes importantes

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Autor

Projeto desenvolvido pela aluna [Zenilda Pedrosa Vieira](https://github.com/ZenildaVieira) da FGA/UnB para a disciplina de TPPE - Tópicos de Programação em Plataformas Emergentes.

---

**Nota**: Este é um projeto acadêmico desenvolvido para fins educacionais.