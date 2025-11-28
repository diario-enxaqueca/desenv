# Banco de Dados – Diário da Enxaqueca

O backend utiliza **MySQL** como banco de dados.  
O script de inicialização se encontra em [`backend/mysql-init/init.sql`](https://github.com/diario-enxaqueca/backend/blob/main/mysql-init/init.sql) e cria as tabelas necessárias para o funcionamento do sistema.



## Estrutura do Banco de Dados

O script define as seguintes tabelas:

- **usuario**: informações de login e identificação de cada usuário.  
- **episodio**: registro dos episódios de enxaqueca de um usuário.  
- **gatilho**: possíveis gatilhos relacionados a um episódio.  
- **medicacao**: medicamentos usados em cada episódio.  
- **dashboard_cache**: cache de estatísticas para melhorar a performance no dashboard.  

## Diagrama do Esquema Físico

Abaixo está a representação visual do DDL:

![Esquema físico do banco de dados](../assets/modelo-fisico.png)

> **Observação:**  
> - Cada **usuário** pode ter vários **episódios**.  
> - Cada **episódio** pode estar relacionado a múltiplos **gatilhos** e múltiplas **medicações**.  
> - A tabela **dashboard_cache** armazena estatísticas globais ou por usuário, dependendo do campo `usuario_id`.  
>
