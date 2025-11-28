# 🎯 MVP — Diário de Enxaqueca

## Objetivo
Fornecer uma aplicação web funcional que permita usuários **registrar, acompanhar e analisar episódios de enxaqueca**, identificando padrões de intensidade, gatilhos e eficácia de medicações.

---

## Escopo do MVP

### Must Have (Essencial para primeira versão)

#### 1. Gestão de Usuários
- ✅ Cadastro de novos usuários
- ✅ Login e autenticação JWT
- ✅ Visualização de perfil
- ✅ Atualização de perfil (Should Have)
- ✅ Exclusão de conta (Could Have)

#### 2. Gestão de Episódios de Enxaqueca
- ✅ Criar episódios (data, intensidade, duração, observações)
- ✅ Listar episódios do usuário
- ✅ Visualizar detalhes completos
- ✅ Editar episódios
- ✅ Excluir episódios

#### 3. Gestão de Gatilhos
- ✅ Cadastrar gatilhos personalizados
- ✅ Listar, editar e excluir gatilhos
- ✅ Associar gatilhos aos episódios

#### 4. Gestão de Medicações
- ✅ Cadastrar medicações
- ✅ Listar, editar e excluir medicações
- ✅ Associar medicações aos episódios

#### 5. Dashboard de Estatísticas
- ✅ Intensidade média dos episódios
- ✅ Total de episódios no mês
- ✅ Gráfico de episódios por mês (últimos 6 meses)
- ✅ Top 5 gatilhos mais frequentes

---

## Características Técnicas

### Backend
- Python 3.10+ com FastAPI
- SQLAlchemy ORM
- MySQL dockerizado
- Arquitetura MVC
- Testes automatizados (pytest)
- Autenticação JWT

### Frontend
- React.js + TypeScript
- Design responsivo
- Integração com API REST
- Componentes reutilizáveis

### Infraestrutura
- Docker e Docker Compose
- CI/CD com GitHub Actions
- Documentação Swagger

---

## Funcionalidades Futuras (Pós-MVP)

### Should Have
- Filtros avançados (intensidade, data, gatilho)
- Busca textual em observações
- Exportação de relatórios PDF

### Could Have
- Notificações e lembretes
- Calendário visual de episódios
- Análise preditiva com ML
- Modo offline (PWA)
- Compartilhamento de relatórios com médicos

---

## Critérios de Sucesso

- ✅ Usuário consegue registrar episódio em < 2 minutos
- ✅ Dashboard carrega em < 3 segundos
- ✅ Sistema suporta 100+ episódios por usuário
- ✅ Taxa de erro < 1%
- ✅ Cobertura de testes > 80%
