# Diário de Enxaqueca - Autenticação

Módulo de autenticação do projeto **Diário de Enxaqueca**, desenvolvido na disciplina Técnicas de Programação em Plataformas Emergentes (TPPE) da FGA/UnB.

Este módulo contém o serviço de autenticação com **FastAPI**, **JWT** e **SQLAlchemy**, responsável pelo gerenciamento de usuários, login, registro e geração de tokens.

## Índice

- [Diário de Enxaqueca - Autenticação](#diário-de-enxaqueca---autenticação)
  - [Índice](#índice)
  - [Visão Geral](#visão-geral)
  - [Arquitetura](#arquitetura)
  - [Tecnologias](#tecnologias)
  - [Estrutura do Projeto](#estrutura-do-projeto)
  - [Ambientes](#ambientes)
    - [Desenvolvimento Local](#desenvolvimento-local)
  - [Instalação e Configuração](#instalação-e-configuração)
    - [Opção 1: Usando Docker (Recomendado)](#opção-1-usando-docker-recomendado)
    - [Opção 2: Desenvolvimento Local sem Docker](#opção-2-desenvolvimento-local-sem-docker)
  - [Executando com Docker](#executando-com-docker)
  - [API](#api)
    - [Documentação Interativa](#documentação-interativa)
    - [Endpoints](#endpoints)
      - [Registro de Usuário](#registro-de-usuário)
      - [Login](#login)
      - [Verificar Token](#verificar-token)
  - [Segurança](#segurança)
    - [Hash de Senhas](#hash-de-senhas)
    - [Tokens JWT](#tokens-jwt)
    - [Validação de Dados](#validação-de-dados)
    - [CORS](#cors)
  - [Testes](#testes)
    - [Executar Testes](#executar-testes)
    - [Estrutura de Testes](#estrutura-de-testes)
  - [Contribuição](#contribuição)
  - [Licença](#licença)

## Visão Geral

O módulo de autenticação fornece uma **API REST para gerenciamento de identidade**, permitindo:

- Registro de novos usuários com validação de dados
- Login com geração de tokens JWT
- Verificação e renovação de tokens
- Gerenciamento de sessões de usuário
- Criptografia de senhas com Argon2
- Integração com backend principal via JWT

Este módulo é separado do backend principal para facilitar escalabilidade e permitir futura extração para um microsserviço independente.

## Arquitetura

O módulo segue o **padrão MVC** com estrutura modular:

- **Model** (`model_auth.py`): Modelo de usuário no banco de dados
- **View** (`view_auth.py`): Rotas da API de autenticação
- **Controller** (`controller_auth.py`): Lógica de negócio (hash, verificação de senha, criação de tokens)
- **Schemas** (`schemas_auth.py`): Validação de dados com Pydantic V2
- **Config** (`config/`): Configurações de banco de dados e variáveis de ambiente

## Tecnologias

- **Python 3.11.14**
- **FastAPI** - Framework web assíncrono
- **SQLAlchemy** - ORM para persistência de dados
- **Pydantic V2** - Validação de dados
- **PyJWT** - Geração e validação de tokens JWT
- **Argon2** - Hash de senhas (CryptContext)
- **MySQL 8** - Banco de dados (compartilhado com backend)
- **pytest** - Framework de testes
- **Docker & Docker Compose** - Containerização

## Estrutura do Projeto

```
autenticacao/
├── auth/
│   ├── controller_auth.py   # Lógica de autenticação
│   ├── model_auth.py         # Modelo de usuário
│   ├── schemas_auth.py       # Schemas de validação
│   ├── view_auth.py          # Rotas da API
│   ├── test_auth.py          # Testes unitários
│   └── test_integration_auth.py  # Testes de integração
├── config/
│   ├── database.py           # Configuração do SQLAlchemy
│   └── settings.py           # Variáveis de ambiente
├── htmlcov/                  # Relatórios de cobertura
├── main.py                   # Ponto de entrada
├── conftest.py               # Configurações do pytest
├── pytest.ini                # Configurações do pytest
├── requirements.txt          # Dependências Python
├── Dockerfile                # Build do container
└── README.md
```

## Ambientes

### Desenvolvimento Local

**Configuração via Docker Compose:**

```env
MYSQL_HOST=db
MYSQL_PORT=3306
MYSQL_USER=diario_user
MYSQL_PASSWORD=********
MYSQL_DB=diario_enxaqueca
MYSQL_USE_SSL=false
SECRET_KEY=dev-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
ENVIRONMENT=development
```
```

**Acesso:**
- API: http://localhost:8001
- Documentação Swagger: http://localhost:8001/docs
- Redoc: http://localhost:8001/redoc

### Produção (Aiven Cloud)

**Configuração com banco gerenciado Aiven:**

```env
MYSQL_HOST=mysql-2e80f044-diario-de-enxaqueca.k.aivencloud.com
MYSQL_PORT=24445
MYSQL_USER=avnadmin
MYSQL_PASSWORD=********
MYSQL_DB=defaultdb
MYSQL_SSL=True
MYSQL_SSL_CA=/app/ca.pem
SECRET_KEY=your-production-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
ENVIRONMENT=production
```

**Características:**
- Banco de dados MySQL gerenciado no Aiven Cloud (compartilhado com backend)
- Tabela `usuarios` compartilhada entre autenticação e backend
- SSL/TLS obrigatório para conexões (certificado ca.pem)
- SECRET_KEY forte e única
- Tokens com expiração configurável

## Instalação e Configuração

### Opção 1: Usando Docker (Recomendado)

Na raiz do projeto (não na pasta autenticacao):

```bash
# Subir todos os serviços
docker-compose up --build -d

# Ver logs do serviço de autenticação
docker-compose logs -f auth

# Verificar status
docker-compose ps
```

### Opção 2: Desenvolvimento Local sem Docker

```bash
cd autenticacao

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate   # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar .env (ajustar MYSQL_HOST para localhost)
cp ../.env .env

# Executar aplicação
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

**Nota:** Certifique-se de ter MySQL rodando e acessível.

## Executando com Docker

```bash
# Subir apenas autenticação + banco de dados
docker-compose up db auth -d

# Ver logs em tempo real
docker-compose logs -f auth

# Parar serviço
docker-compose stop auth

# Reiniciar
docker-compose restart auth
```

## API

### Documentação Interativa

- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

### Endpoints

#### Registro de Usuário

```http
POST /api/auth/register
Content-Type: application/json

{
  "nome": "João Silva",
  "email": "joao@example.com",
  "senha": "senhaSegura123"
}
```

**Resposta (201 Created):**
```json
{
  "id": 1,
  "nome": "João Silva",
  "email": "joao@example.com",
  "data_cadastro": "2025-11-26T10:30:00"
}
```

#### Login

```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "joao@example.com",
  "senha": "senhaSegura123"
}
```

**Resposta (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "nome": "João Silva",
    "email": "joao@example.com"
  }
}
```

#### Verificar Token

```http
GET /api/auth/me
Authorization: Bearer <token>
```

**Resposta (200 OK):**
```json
{
  "id": 1,
  "nome": "João Silva",
  "email": "joao@example.com",
  "data_cadastro": "2025-11-26T10:30:00"
}
```

## Segurança

### Hash de Senhas

- **Algoritmo:** Argon2 (via `passlib.CryptContext`)
- **Configuração:** `schemes=["argon2"], deprecated="auto"`
- Senhas são truncadas em 72 bytes antes do hash
- Senhas nunca são armazenadas em texto plano

### Tokens JWT

- **Algoritmo:** HS256 (HMAC with SHA-256)
- **Expiração:** 1440 minutos (24 horas) por padrão
- **Payload:** `{"sub": "email@example.com", "exp": timestamp}`
- **Validação:** Verificação de assinatura e expiração em cada request

### Validação de Dados

- **Email:** Validado com Pydantic `EmailStr`
- **Senha:** Mínimo 8 caracteres, máximo 72
- **Nome:** Mínimo 3 caracteres, máximo 100

### CORS

Configurado para aceitar requests do frontend:
- Desenvolvimento: `http://localhost:3000`
- Produção: Domínio configurado via variável de ambiente

## Testes

### Executar Testes

```bash
# Via Docker (recomendado)
docker-compose run --rm tests-auth

# Com relatório de cobertura
docker-compose run --rm tests-auth pytest --cov=auth --cov-report=html

# Localmente
cd autenticacao
pytest
pytest --cov=auth --cov-report=term-missing
```

### Estrutura de Testes

- **`test_auth.py`**: Testes unitários de hash, verificação de senha, criação de usuários
- **`test_integration_auth.py`**: Testes de integração com endpoints completos

**Cobertura:** Inclusa na cobertura geral do projeto (95%)

## Contribuição

Contribuições são bem-vindas! Siga as mesmas diretrizes do projeto principal:

1. Fork o repositório
2. Crie branch a partir da `main`
3. Desenvolva seguindo padrão MVC
4. Adicione testes para novas funcionalidades
5. Execute testes antes de abrir PR
6. Use **Conventional Commits**
7. Abra Pull Request com descrição clara

**Padrões de Segurança:**
- Nunca commitar chaves secretas ou senhas
- Usar variáveis de ambiente para dados sensíveis
- Manter dependências atualizadas
- Validar todos os inputs do usuário

## Licença

MIT License © [ZenildaVieira](https://github.com/ZenildaVieira)