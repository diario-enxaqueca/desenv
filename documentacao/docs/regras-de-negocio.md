# Regras de Negócio — Diário de Enxaqueca

Este documento define as regras de negócio do sistema **Diário de Enxaqueca**, descrevendo validações, restrições, cálculos e comportamentos esperados para cada entidade do sistema.

---

## Sumário

1. [Usuários](#1-usuários)
2. [Episódios de Enxaqueca](#2-episódios-de-enxaqueca)
3. [Gatilhos](#3-gatilhos)
4. [Medicações](#4-medicações)
5. [Dashboard e Estatísticas](#5-dashboard-e-estatísticas)
6. [Autenticação e Autorização](#6-autenticação-e-autorização)
7. [Validações Gerais](#7-validações-gerais)
8. [Códigos HTTP](#8-códigos-http)

---

## 1. Usuários

### BR-001: Unicidade de E-mail
**Descrição:** O e-mail de cada usuário deve ser único no sistema.  
**Regra:**  
```
SE um novo usuário tenta se cadastrar com e-mail já existente
ENTÃO o sistema retorna erro 400 (Bad Request)
E exibe mensagem: "E-mail já cadastrado"
```
**Validação:** Verificação no banco antes da criação/atualização.

---

### BR-002: Formato de E-mail
**Descrição:** O e-mail deve seguir o formato padrão (ex: `usuario@dominio.com`).  
**Regra:**  
```
SE o e-mail não contém "@" e domínio válido
ENTÃO o sistema retorna erro 400
E exibe mensagem: "Formato de e-mail inválido"
```
**Validação:** Regex: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`

---

### BR-003: Senha Mínima
**Descrição:** A senha deve ter no mínimo 8 caracteres.  
**Regra:**  
```
SE a senha possui menos de 8 caracteres
ENTÃO o sistema retorna erro 400
E exibe mensagem: "Senha deve ter no mínimo 8 caracteres"
```
**Recomendação:** Incluir ao menos uma letra maiúscula, um número e um caractere especial (Could Have).

---

### BR-004: Criptografia de Senha
**Descrição:** Senhas devem ser armazenadas de forma criptografada (hash).  
**Regra:**  
```
QUANDO um usuário cria ou atualiza senha
ENTÃO o sistema deve aplicar hash bcrypt ou Argon2
E nunca armazenar senha em texto plano
```
**Implementação:** Usar biblioteca `bcrypt` ou `passlib`.

---

### BR-005: Edição de Dados de Usuário
**Descrição:** Usuário só pode editar seus próprios dados.  
**Regra:**  
```
SE usuário tenta editar dados de outro usuário
ENTÃO o sistema retorna erro 403 (Forbidden)
E exibe mensagem: "Acesso negado"
```
**Exceção:** Administrador pode editar qualquer usuário.

---

### BR-006: Exclusão de Conta
**Descrição:** Ao excluir conta, todos os episódios associados são removidos.  
**Regra:**  
```
QUANDO usuário confirma exclusão de conta
ENTÃO o sistema remove:
  - Registro do usuário
  - Todos os episódios vinculados
  - Gatilhos e medicações personalizados
E retorna código 204 (No Content)
```
**Validação:** Confirmação obrigatória antes da exclusão.

---

## 2. Episódios de Enxaqueca

### BR-007: Vinculação de Episódio a Usuário
**Descrição:** Cada episódio pertence obrigatoriamente a um usuário.  
**Regra:**  
```
SE episódio for criado sem `usuario_id`
ENTÃO o sistema retorna erro 400
E exibe mensagem: "Usuário não identificado"
```
**Validação:** `usuario_id` deve existir na tabela `usuarios`.

---

### BR-008: Data do Episódio Obrigatória
**Descrição:** A data do episódio é obrigatória e não pode ser futura.  
**Regra:**  
```
SE data está vazia OU data > data atual
ENTÃO o sistema retorna erro 400
E exibe mensagem: "Data inválida ou futura"
```
**Validação:** Comparação com `datetime.now()`.

---

### BR-009: Intensidade Válida
**Descrição:** A intensidade deve ser um número inteiro entre 0 e 10.  
**Regra:**  
```
SE intensidade < 0 OU intensidade > 10 OU não é número
ENTÃO o sistema retorna erro 400
E exibe mensagem: "Intensidade deve ser entre 0 e 10"
```
**Validação:** Tipo `int`, range validado.

---

### BR-010: Duração do Episódio
**Descrição:** Duração é opcional, mas se informada, deve ser em minutos (inteiro positivo).  
**Regra:**  
```
SE duração < 0 OU não é número inteiro
ENTÃO o sistema retorna erro 400
E exibe mensagem: "Duração inválida"
```
**Validação:** Tipo `int`, valor >= 0.

---

### BR-011: Gatilhos Múltiplos
**Descrição:** Um episódio pode ter múltiplos gatilhos ou nenhum.  
**Regra:**  
```
SE gatilhos forem informados
ENTÃO cada gatilho deve existir na tabela `gatilhos` do usuário
SENÃO campo pode ficar vazio
```
**Relação:** Many-to-Many via tabela intermediária `episodio_gatilho`.

---

### BR-012: Medicações Múltiplas
**Descrição:** Um episódio pode ter múltiplas medicações ou nenhuma.  
**Regra:**  
```
SE medicações forem informadas
ENTÃO cada medicação deve existir na tabela `medicacoes` do usuário
SENÃO campo pode ficar vazio
```
**Relação:** Many-to-Many via tabela intermediária `episodio_medicacao`.

---

### BR-013: Observações Limitadas
**Descrição:** Campo `observacoes` pode ter no máximo 500 caracteres.  
**Regra:**  
```
SE comprimento(observacoes) > 500
ENTÃO o sistema retorna erro 400
E exibe mensagem: "Observações excedem 500 caracteres"
```
**Validação:** String length check.

---

### BR-014: Permissão de Edição/Exclusão
**Descrição:** Usuário só pode editar/excluir seus próprios episódios.  
**Regra:**  
```
SE usuário tenta editar/excluir episódio de outro usuário
ENTÃO o sistema retorna erro 403
E exibe mensagem: "Acesso negado"
```
**Validação:** Verificar `episodio.usuario_id == usuario_logado.id`.

---

### BR-015: Listagem de Episódios
**Descrição:** Episódios devem ser listados em ordem decrescente de data (mais recente primeiro).  
**Regra:**  
```
QUANDO usuário solicita lista de episódios
ENTÃO o sistema retorna episódios ordenados por `data DESC`
E aplica paginação de 10 registros por página
```
**Implementação:** SQL `ORDER BY data DESC LIMIT 10 OFFSET n`.

---

### BR-016: Persistência no Banco
**Descrição:** Ao criar episódio, dados devem ser persistidos no MySQL.  
**Regra:**  
```
QUANDO episódio é criado com sucesso
ENTÃO sistema retorna código 201 (Created)
E retorna JSON com `id`, `data`, `intensidade` e demais campos
```

---

## 3. Gatilhos

### BR-017: Gatilhos Personalizados
**Descrição:** Cada usuário pode criar seus próprios gatilhos.  
**Regra:**  
```
QUANDO usuário cria gatilho
ENTÃO o gatilho fica disponível apenas para esse usuário
E deve ter nome único dentro do escopo do usuário
```
**Validação:** Unicidade de `nome` por `usuario_id`.

---

### BR-018: Nome de Gatilho Único
**Descrição:** Nome do gatilho deve ser único por usuário.  
**Regra:**  
```
SE usuário tenta criar gatilho com nome já existente (dele)
ENTÃO o sistema retorna erro 400
E exibe mensagem: "Gatilho já cadastrado"
```

---

### BR-019: Exclusão de Gatilho
**Descrição:** Ao excluir gatilho, associações com episódios são removidas.  
**Regra:**  
```
QUANDO gatilho é excluído
ENTÃO registros em `episodio_gatilho` relacionados são removidos
E episódios não são afetados
```
**Implementação:** `ON DELETE CASCADE` na FK.

---

## 4. Medicações

### BR-020: Medicações Personalizadas
**Descrição:** Cada usuário pode criar suas próprias medicações.  
**Regra:**  
```
QUANDO usuário cria medicação
ENTÃO a medicação fica disponível apenas para esse usuário
E deve ter nome único dentro do escopo do usuário
```
**Validação:** Unicidade de `nome` por `usuario_id`.

---

### BR-021: Nome de Medicação Único
**Descrição:** Nome da medicação deve ser único por usuário.  
**Regra:**  
```
SE usuário tenta criar medicação com nome já existente (dele)
ENTÃO o sistema retorna erro 400
E exibe mensagem: "Medicação já cadastrada"
```

---

### BR-022: Dosagem Opcional
**Descrição:** Campo `dosagem` é opcional (ex: "500mg", "1 comprimido").  
**Regra:**  
```
SE dosagem for informada
ENTÃO armazenar como string (máximo 100 caracteres)
SENÃO pode ficar vazio (NULL)
```

---

### BR-023: Exclusão de Medicação
**Descrição:** Ao excluir medicação, associações com episódios são removidas.  
**Regra:**  
```
QUANDO medicação é excluída
ENTÃO registros em `episodio_medicacao` relacionados são removidos
E episódios não são afetados
```
**Implementação:** `ON DELETE CASCADE` na FK.

---

## 5. Dashboard e Estatísticas

### BR-024: Dados do Usuário Logado
**Descrição:** Dashboard mostra apenas episódios do usuário logado.  
**Regra:**  
```
QUANDO usuário acessa dashboard
ENTÃO o sistema filtra episódios WHERE `usuario_id` = id do usuário logado
```

---

### BR-025: Cálculo de Intensidade Média
**Descrição:** Intensidade média é calculada sobre todos os episódios do usuário.  
**Regra:**  
```
Intensidade Média = SUM(intensidade) / COUNT(episodios)
ONDE usuario_id = id do usuário logado
```
**Precisão:** 2 casas decimais.

---

### BR-026: Total de Episódios no Mês
**Descrição:** Contabilizar episódios do mês atual.  
**Regra:**  
```
Total = COUNT(episodios)
ONDE usuario_id = id do usuário logado
E MONTH(data) = mês atual
E YEAR(data) = ano atual
```

---

### BR-027: Gatilhos Mais Frequentes
**Descrição:** Listar os 5 gatilhos mais associados a episódios.  
**Regra:**  
```
SELECT gatilho.nome, COUNT(*) as frequencia
FROM episodio_gatilho
JOIN gatilhos ON gatilho_id = gatilhos.id
WHERE episodio.usuario_id = id do usuário logado
GROUP BY gatilho.nome
ORDER BY frequencia DESC
LIMIT 5
```

---

### BR-028: Gráfico de Episódios por Mês
**Descrição:** Mostrar episódios dos últimos 6 meses.  
**Regra:**  
```
SELECT MONTH(data) as mes, COUNT(*) as total
FROM episodios
WHERE usuario_id = id do usuário logado
E data >= (data_atual - 6 meses)
GROUP BY MONTH(data)
ORDER BY data ASC
```

---

### BR-029: Filtros Aplicáveis
**Descrição:** Filtros (intensidade, data) só se aplicam aos episódios do usuário logado.  
**Regra:**  
```
SE usuário aplica filtro de intensidade OU período
ENTÃO o sistema filtra apenas episódios WHERE usuario_id = id do usuário
```

---

## 6. Autenticação e Autorização

### BR-030: Token JWT
**Descrição:** Autenticação via JWT com expiração de 24 horas.  
**Regra:**  
```
QUANDO usuário faz login com credenciais corretas
ENTÃO o sistema gera token JWT válido por 24 horas
E retorna token no campo `access_token`
```
**Implementação:** Biblioteca `PyJWT` ou `python-jose`.

---

### BR-031: Acesso a Rotas Protegidas
**Descrição:** Rotas protegidas exigem token JWT válido.  
**Regra:**  
```
SE requisição não contém token OU token expirado/inválido
ENTÃO o sistema retorna erro 401 (Unauthorized)
E exibe mensagem: "Token inválido ou expirado"
```
**Header:** `Authorization: Bearer <token>`.

---

### BR-032: Logout
**Descrição:** Logout invalida o token no cliente (sem blacklist no MVP).  
**Regra:**  
```
QUANDO usuário faz logout
ENTÃO o frontend remove token do armazenamento local
```
**Nota:** Backend stateless (sem blacklist de tokens no MVP).

---

## 7. Validações Gerais

### BR-033: Campos Obrigatórios
**Descrição:** Campos obrigatórios devem ser preenchidos antes do envio.  
**Regra:**  
```
SE algum campo obrigatório está vazio
ENTÃO o sistema retorna erro 400
E exibe mensagem: "Campo {nome_campo} é obrigatório"
```
**Validação:** Pydantic schemas com `required=True`.

---

### BR-034: Mensagens de Erro Claras
**Descrição:** Mensagens de erro devem ser claras e específicas.  
**Regra:**  
```
QUANDO ocorre erro de validação
ENTÃO o sistema retorna JSON com:
{
  "detail": "Descrição clara do erro",
  "field": "nome_do_campo" (quando aplicável)
}
```

---

### BR-035: Formato de Data
**Descrição:** Datas devem estar no formato ISO 8601 (`YYYY-MM-DD`).  
**Regra:**  
```
SE data não está no formato YYYY-MM-DD
ENTÃO o sistema retorna erro 400
E exibe mensagem: "Formato de data inválido. Use YYYY-MM-DD"
```

---

### BR-036: Integridade Referencial
**Descrição:** Foreign Keys devem referenciar registros existentes.  
**Regra:**  
```
SEFK referencia registro inexistente
ENTÃO o sistema retorna erro 400
E exibe mensagem: "{Entidade} não encontrado(a)"
```
**Implementação:** Constraints do MySQL.

---

## 8. Códigos HTTP

### BR-037: Códigos de Status Padrão
**Descrição:** Backend deve retornar códigos HTTP apropriados.  

| Código | Descrição | Uso |
|--------|-----------|-----|
| 200 | OK | Requisição bem-sucedida (GET, PUT) |
| 201 | Created | Recurso criado com sucesso (POST) |
| 204 | No Content | Exclusão bem-sucedida (DELETE) |
| 400 | Bad Request | Erro de validação ou requisição inválida |
| 401 | Unauthorized | Token ausente ou inválido |
| 403 | Forbidden | Sem permissão para acessar recurso |
| 404 | Not Found | Recurso não encontrado |
| 500 | Internal Server Error | Erro inesperado no servidor |

---

## 9. Referências

- [RFC 7231 - HTTP Status Codes](https://tools.ietf.org/html/rfc7231)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
- [ISO 8601 - Date Format](https://www.iso.org/iso-8601-date-and-time-format.html)
- Documentação FastAPI: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)

---

## 10. Controle de Versão

| Versão | Data | Autor | Alterações |
|--------|------|-------|------------|
| 1.0 | 2025-10-24 | Equipe Diário de Enxaqueca | Versão inicial |

---

**Nota:** Este documento deve ser revisado e atualizado regularmente para refletir mudanças nos requisitos de negócio.

