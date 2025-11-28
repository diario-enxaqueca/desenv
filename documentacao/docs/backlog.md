# 📋 Backlog — Histórias de Usuário

## Resumo
Total de histórias: **21**  
Prioridade Must Have: **11**  
Prioridade Should Have: **8**  
Prioridade Could Have: **2**

---

## Entidade 1: Usuário

### US-01: Cadastro de Usuário (Must Have)
**Como** visitante  
**Quero** me cadastrar no sistema  
**Para** criar minha conta e começar a registrar episódios

**Critérios de Aceitação:**
- **Given** que estou na página de registro
- **When** preencho nome, email e senha válidos
- **Then** minha conta é criada e sou redirecionado ao login
- **And** recebo confirmação de cadastro

**Validações:**
- Email único
- Senha mínima de 8 caracteres
- Nome obrigatório

---

### US-02: Login de Usuário (Must Have)
**Como** usuário cadastrado  
**Quero** fazer login  
**Para** acessar meus dados

**Critérios de Aceitação:**
- **Given** que tenho uma conta cadastrada
- **When** insiro email e senha corretos
- **Then** recebo um token JWT válido
- **And** sou redirecionado ao dashboard

**Validações:**
- Credenciais corretas
- Token expira em 24h

---

### US-03: Visualizar Perfil (Must Have)
**Como** usuário logado  
**Quero** visualizar meu perfil  
**Para** ver minhas informações

**Critérios de Aceitação:**
- **Given** que estou logado
- **When** acesso a página de perfil
- **Then** vejo meu nome, email e data de cadastro
- **And** posso acessar opção de editar

---

### US-04: Editar Perfil (Should Have)
**Como** usuário logado  
**Quero** editar meu perfil  
**Para** atualizar meus dados

**Critérios de Aceitação:**
- **Given** que estou na página de perfil
- **When** altero nome ou email
- **Then** as alterações são salvas
- **And** vejo mensagem de confirmação

**Validações:**
- Email único

---

### US-05: Excluir Conta (Could Have)
**Como** usuário logado  
**Quero** excluir minha conta  
**Para** remover todos os meus dados

**Critérios de Aceitação:**
- **Given** que estou na página de configurações
- **When** confirmo exclusão da conta
- **Then** minha conta e todos os episódios são removidos
- **And** sou redirecionado à página inicial

**Validações:**
- Confirmação obrigatória

---

## Entidade 2: Episódio de Enxaqueca

### US-06: Criar Episódio (Must Have)
**Como** usuário logado  
**Quero** criar um episódio de enxaqueca  
**Para** registrar o que aconteceu

**Critérios de Aceitação:**
- **Given** que estou na página de criar episódio
- **When** preencho data, intensidade (0-10) e duração
- **Then** o episódio é salvo
- **And** sou redirecionado à lista de episódios

**Campos:**
- **Obrigatórios:** data, intensidade
- **Opcionais:** duração, gatilhos, medicações, observações

---

### US-07: Listar Episódios (Must Have)
**Como** usuário logado  
**Quero** listar meus episódios  
**Para** ver meu histórico

**Critérios de Aceitação:**
- **Given** que estou logado
- **When** acesso a página de episódios
- **Then** vejo lista ordenada por data (mais recente primeiro)
- **And** cada item mostra data, intensidade e resumo

**Paginação:** 10 episódios por página

---

### US-08: Visualizar Episódio (Must Have)
**Como** usuário logado  
**Quero** visualizar detalhes de um episódio específico  
**Para** ver todas as informações

**Critérios de Aceitação:**
- **Given** que estou na lista de episódios
- **When** clico em um episódio
- **Then** vejo todos os campos: data, intensidade, duração, gatilhos, medicações, observações
- **And** posso acessar opção de editar ou excluir

---

### US-09: Editar Episódio (Must Have)
**Como** usuário logado  
**Quero** editar um episódio existente  
**Para** corrigir informações

**Critérios de Aceitação:**
- **Given** que estou visualizando um episódio
- **When** altero qualquer campo e salvo
- **Then** as alterações são persistidas
- **And** vejo mensagem de confirmação

**Validações:** mesmas da criação

---

### US-10: Excluir Episódio (Must Have)
**Como** usuário logado  
**Quero** excluir um episódio  
**Para** remover registros incorretos

**Critérios de Aceitação:**
- **Given** que estou visualizando um episódio
- **When** confirmo a exclusão
- **Then** o episódio é removido do banco
- **And** sou redirecionado à lista atualizada

**Validações:** confirmação obrigatória

---

## Entidade 3: Gatilho

### US-11: Cadastrar Gatilho (Should Have)
**Como** usuário logado  
**Quero** cadastrar gatilhos personalizados  
**Para** associá-los aos episódios

**Critérios de Aceitação:**
- **Given** que estou na página de gatilhos
- **When** adiciono nome do gatilho (ex: "Estresse", "Chocolate")
- **Then** o gatilho é salvo
- **And** fica disponível para seleção nos episódios

**Validações:** nome único por usuário

---

### US-12: Listar Gatilhos (Should Have)
**Como** usuário logado  
**Quero** listar meus gatilhos cadastrados  
**Para** gerenciá-los

**Critérios de Aceitação:**
- **Given** que estou na página de gatilhos
- **When** acesso a lista
- **Then** vejo todos os gatilhos ordenados alfabeticamente
- **And** posso editar ou excluir cada um

---

### US-13: Editar Gatilho (Should Have)
**Como** usuário logado  
**Quero** editar um gatilho  
**Para** corrigir o nome

**Critérios de Aceitação:**
- **Given** que estou na lista de gatilhos
- **When** altero o nome de um gatilho
- **Then** a alteração é salva
- **And** reflete em todos os episódios associados

---

### US-14: Excluir Gatilho (Should Have)
**Como** usuário logado  
**Quero** excluir um gatilho que não uso mais  
**Para** manter minha lista organizada

**Critérios de Aceitação:**
- **Given** que estou na lista de gatilhos
- **When** confirmo exclusão
- **Then** o gatilho é removido
- **And** associações com episódios são removidas

**Validações:** confirmação obrigatória

---

## Entidade 4: Medicação

### US-15 a US-18: [Seguem o mesmo padrão CRUD dos Gatilhos]

---

## Entidade 5: Dashboard

### US-19: Dashboard de Estatísticas (Must Have)
**Como** usuário logado  
**Quero** ver um dashboard com estatísticas dos meus episódios  
**Para** entender padrões

**Critérios de Aceitação:**
- **Given** que estou logado
- **When** acesso o dashboard
- **Then** vejo:
  - Intensidade média
  - Total de episódios no mês
  - Gráfico de episódios por mês (últimos 6 meses)
  - Lista dos 5 gatilhos mais frequentes

---

### US-20 e US-21: Filtros (Could Have)
[Filtros por intensidade e período]

---

## Priorização (MoSCoW)

| Prioridade | Total | Histórias |
|------------|-------|-----------|
| Must Have | 11 | US-01 a US-03, US-06 a US-10, US-19 |
| Should Have | 8 | US-04, US-11 a US-18 |
| Could Have | 2 | US-05, US-20, US-21 |
