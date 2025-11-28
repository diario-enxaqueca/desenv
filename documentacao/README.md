# Diário de Enxaqueca - Documentação

Repositório de documentação do projeto **Diário de Enxaqueca**, desenvolvido na disciplina Técnicas de Programação em Plataformas Emergentes (TPPE) da FGA/UnB.

Este repositório organiza todas as informações do projeto, incluindo MVP, backlog, regras de negócio, diagramas UML, protótipo Figma e guias de desenvolvimento, garantindo rastreabilidade e suporte para desenvolvimento.

## Índice

- [Visão Geral](#visão-geral)
- [Arquitetura do Projeto](#arquitetura-do-projeto)
- [Estrutura da Documentação](#estrutura-da-documentação)
- [Conteúdo Disponível](#conteúdo-disponível)
- [Deploy em Produção](#deploy-em-produção)
- [Desenvolvimento Local](#desenvolvimento-local)
- [Links do Projeto](#links-do-projeto)
- [Boas Práticas](#boas-práticas)
- [Contribuição](#contribuição)

## Visão Geral

O projeto Diário de Enxaqueca é uma aplicação completa para registro e acompanhamento de episódios de enxaqueca, desenvolvida com arquitetura **MVC modular** preparada para futura migração para microsserviços.

**Objetivo da documentação:**
- Organizar e detalhar todas as fases do projeto
- Garantir rastreabilidade de requisitos
- Fornecer guias de desenvolvimento e deploy
- Documentar decisões arquiteturais e de design
- Facilitar onboarding de novos contribuidores

## Arquitetura do Projeto

O projeto utiliza **arquitetura MVC (Model-View-Controller)** modular, com estrutura de pastas preparada para futura migração para microsserviços. Cada módulo possui separação clara de responsabilidades seguindo o padrão MVC.

### Componentes

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Frontend  │─────▶│   Backend    │─────▶│    MySQL    │
│  (React)    │      │   MVC API    │      │  Database   │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │     Auth     │
                     │   Module     │
                     └──────────────┘
```

- **Frontend** (`frontend/`): Interface React + Vite + TypeScript + Tailwind CSS
- **Backend** (`backend/`): API REST com FastAPI + SQLAlchemy + MySQL
  - Módulos MVC: episodio, gatilho, medicacao, usuario
- **Autenticação** (`autenticacao/`): Módulo separado de autenticação JWT
- **Banco de Dados**: MySQL 8 dockerizado com healthcheck

### Tecnologias

**Backend:**
- Python 3.11.14, FastAPI, SQLAlchemy, Pydantic V2
- pytest (cobertura 95%), Pylint (nota 8.91/10)

**Frontend:**
- React 18, Vite, TypeScript, Tailwind CSS
- Selenium (testes E2E)

**Infraestrutura:**
- Docker & Docker Compose
- MySQL 8
- Nginx (frontend em produção)

## Estrutura da Documentação

```
documentacao/
├── docs/                    # Documentos do projeto
│   ├── backlog.md          # Histórias de usuário
│   ├── mvp.md              # Definição do MVP
│   ├── regras-de-negocio.md # Regras funcionais
│   ├── guia-de-estilo.md   # Identidade visual
│   ├── prototipo.md        # Link e descrição do Figma
│   ├── ddl.sql             # DDL do banco de dados
│   ├── modelo-fisico.md    # Modelo físico do banco
│   └── ...                 # Outros documentos
├── assets/                  # Recursos visuais
│   ├── logos/              # Logo do projeto
│   ├── paleta-cores/       # Paleta de cores
│   └── icones/             # Ícones da aplicação
├── CONTRIBUTING.md          # Guia de contribuição
├── LICENSE                  # Licença MIT
└── README.md               # Este arquivo
```

## Conteúdo Disponível

### Design e UX

- **[Guia de Estilo](https://github.com/diario-enxaqueca/desenvolvimento/blob/main/documentacao/docs/guia-de-estilo.md):** Identidade visual completa (logo, paleta de cores, tipografia, iconografia)
- **[Protótipo Figma](https://github.com/diario-enxaqueca/desenvolvimento/blob/main/documentacao/docs/prototipo.md):** Design de alta fidelidade das interfaces
  - Link: [Figma - Diário de Enxaqueca App](https://www.figma.com/design/1DMxk1tsucSCuyq63F3Pg2/Di%C3%A1rio-de-Enxaqueca-App)

### Planejamento

- **[MVP](https://github.com/diario-enxaqueca/desenvolvimento/blob/main/documentacao/docs/mvp.md):** Definição do Produto Mínimo Viável
- **[Backlog](https://github.com/diario-enxaqueca/desenvolvimento/blob/main/documentacao/docs/backlog.md):** Histórias de usuário (mínimo de 10)
- **[Regras de Negócio](https://github.com/diario-enxaqueca/desenvolvimento/blob/main/documentacao/docs/regras-de-negocio.md):** Descrição funcional do sistema

### Banco de Dados

- **[DDL](https://github.com/diario-enxaqueca/desenvolvimento/blob/main/documentacao/docs/ddl.sql):** Script de criação do banco de dados
- **[Modelo Físico](https://github.com/diario-enxaqueca/desenvolvimento/blob/main/documentacao/docs/modelo-fisico.md):** Documentação da estrutura do banco

### Guias de Desenvolvimento

- **README principal:** [README.md](https://github.com/diario-enxaqueca/desenvolvimento/blob/main/README.md) - Visão geral e setup do projeto
- **Backend:** [backend/README.md](https://github.com/diario-enxaqueca/desenvolvimento/blob/main/backend/README.md) - Documentação da API
- **Frontend:** [frontend/README.md](https://github.com/diario-enxaqueca/desenvolvimento/blob/main/frontend/README.md) - Documentação da interface
- **Autenticação:** [autenticacao/README.md](https://github.com/diario-enxaqueca/desenvolvimento/blob/main/autenticacao/README.md) - Documentação do módulo auth

## Deploy em Produção

### Banco de Dados Aiven

O projeto utiliza MySQL gerenciado no Aiven Cloud para produção:

```env
MYSQL_HOST=mysql-2e80f044-diario-de-enxaqueca.k.aivencloud.com
MYSQL_PORT=24445
MYSQL_USER=avnadmin
MYSQL_PASSWORD=********
MYSQL_DB=defaultdb
MYSQL_SSL=True
MYSQL_SSL_CA=/app/ca.pem
```

**Características:**
- Banco compartilhado entre backend e autenticação
- SSL/TLS obrigatório (certificado ca.pem)
- Backup automático
- Monitoramento 24/7

### Railway (Recomendado)

O projeto está configurado para deploy no Railway com os seguintes serviços:

#### 1. Backend Service

```env
MYSQL_HOST=mysql-2e80f044-diario-de-enxaqueca.k.aivencloud.com
MYSQL_PORT=24445
MYSQL_USER=avnadmin
MYSQL_PASSWORD=********
MYSQL_DB=defaultdb
MYSQL_SSL=True
MYSQL_SSL_CA=/app/ca.pem
SECRET_KEY=production-secret-key
ENVIRONMENT=production
DEBUG=false
```

**URL:** https://backend-production-f9d7.up.railway.app

#### 2. Auth Service

```env
MYSQL_HOST=mysql-2e80f044-diario-de-enxaqueca.k.aivencloud.com
MYSQL_PORT=24445
MYSQL_USER=avnadmin
MYSQL_PASSWORD=********
MYSQL_DB=defaultdb
MYSQL_SSL=True
MYSQL_SSL_CA=/app/ca.pem
SECRET_KEY=production-secret-key
SECRET_KEY=production-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
ENVIRONMENT=production
```

**URL:** https://autenticacao-production-00f7.up.railway.app

#### 3. Frontend Service

```env
VITE_BACKEND_URL=https://backend-production-f9d7.up.railway.app/api
VITE_AUTH_URL=https://autenticacao-production-00f7.up.railway.app/api/auth
```

**URL:** https://frontend-production-7dfd.up.railway.app

### Passos para Deploy

1. **Conectar Repositório GitHub ao Railway**
   - Criar conta no [Railway](https://railway.app)
   - Conectar repositório GitHub
   - Railway detectará automaticamente os serviços

2. **Configurar Variáveis de Ambiente**
   - Configurar cada serviço conforme exemplos acima
   - Garantir que SECRET_KEY seja forte e única

3. **Configurar Domínio (Opcional)**
   - Settings > Domains
   - Adicionar domínio customizado

4. **Verificar Deploy**
   - Acessar URLs dos serviços
   - Testar login/cadastro
   - Verificar conectividade entre serviços

## Desenvolvimento Local

### Pré-requisitos

- **Docker Desktop** (Windows/Mac) ou Docker Engine (Linux)
- **Git** para clonar repositório
- **Node.js 18+** (opcional, para desenvolvimento frontend)
- **Python 3.11+** (opcional, para desenvolvimento backend)

### Quick Start

```bash
# Clonar repositório
git clone https://github.com/diario-enxaqueca/desenvolvimento.git
cd desenvolvimento

# Subir todos os serviços
docker-compose up --build -d

# Verificar status
docker-compose ps

# Ver logs
docker-compose logs -f
```

### Endpoints Locais

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **Backend Docs:** http://localhost:8000/docs
- **Auth Service:** http://localhost:8001
- **Auth Docs:** http://localhost:8001/docs
- **Database:** localhost:3306

### Ambiente de Desenvolvimento vs Produção

| Variável | Desenvolvimento | Produção |
|----------|----------------|----------|
| MYSQL_HOST | db | mysql-2e80f044-diario-de-enxaqueca.k.aivencloud.com |
| MYSQL_PORT | 3306 | 24445 |
| MYSQL_SSL | false | True |
| BACKEND_URL | http://localhost:8000 | https://backend-production.railway.app |
| DEBUG | true | false |

### Scripts de Automação

O projeto inclui scripts PowerShell para facilitar operações:

```powershell
# Capturar logs de todos os serviços
.\scripts\capture-logs.ps1

# Parar serviços
.\scripts\stop-logs.ps1

# Rebuild completo + todos os testes + logs
.\scripts\stop-then-capture-logs-com-build-no-cache.ps1
```

**Detalhes:** Consulte `/README.md` seção "Scripts de Automação"

## Links do Projeto

### Repositórios

- [Organização GitHub](https://github.com/diario-enxaqueca)
- [Desenvolvimento (Monorepo)](https://github.com/diario-enxaqueca/desenvolvimento)
- [Documentação](https://github.com/diario-enxaqueca/documentacao)

### Protótipo e Design

- [Figma - Diário de Enxaqueca App](https://www.figma.com/design/1DMxk1tsucSCuyq63F3Pg2/Di%C3%A1rio-de-Enxaqueca-App)

### Deploy em Produção

- [Frontend](https://frontend-production-7dfd.up.railway.app)
- [Backend](https://backend-production-f9d7.up.railway.app)
- [Autenticação](https://autenticacao-production-00f7.up.railway.app)

## Boas Práticas

### Documentação

- Toda documentação segue **ABNT NBR 6023:2020** para referências
- Diagramas UML criados com **Draw.io**
- Protótipos desenvolvidos no **Figma**
- Markdown para documentos técnicos

### Versionamento

- Commits seguem **Conventional Commits**
- Branches criadas a partir de `main`
- Pull Requests com revisão obrigatória
- Tags para releases importantes

### Qualidade

- Cobertura de testes: 95%
- Pylint score: 8.91/10
- Todos os PRs passam por testes automatizados
- Documentação atualizada junto com código

## Contribuição

Contribuições são bem-vindas! Para manter consistência e qualidade:

1. **Fork** o repositório
2. **Clone** seu fork
3. Crie uma **branch** (`git checkout -b feature/NovaDoc`)
4. **Desenvolva** sua contribuição
5. Siga os **padrões de documentação**
6. **Commit** com mensagens claras (`docs: adiciona diagrama de atividades`)
7. **Push** para sua branch
8. Abra **Pull Request**

**Guia completo:** [CONTRIBUTING.md](https://github.com/diario-enxaqueca/desenvolvimento/blob/main/documentacao/CONTRIBUTING.md)

### Padrões para Documentação

- Usar Markdown para documentos técnicos
- Incluir data de última atualização
- Adicionar referências quando aplicável
- Manter consistência de formatação
- Atualizar índice ao adicionar seções

## Licença

Este projeto está sob a licença MIT.

[MIT License](https://github.com/diario-enxaqueca/desenvolvimento/blob/main/documentacao/LICENSE) © [ZenildaVieira](https://github.com/ZenildaVieira)

---

**Nota:** Este é um projeto acadêmico desenvolvido para fins educacionais na FGA/UnB.
