# Ponto de Controle 1

* Diagrama DDL e script SQL
  * [Diagrama Lógico](./docs/diagrama-logico.md)
* Backlog
  * [Backlog](./docs/backlog.md)
* Protótipo de Alta Fidelidade
  * [Protótipo](./docs/prototipo.md)
* Docker
  * [docker-compose.yml](./docker-compose.yml)

# Ponto de Controle 2

* Arquitetura
  * [README.md/Arquitetura](https://github.com/diario-enxaqueca/documentacao/blob/main/README.md#arquitetura-do-projeto)  
  
* Clean Code
  * [README.md/Estrutura do Projeto](https://github.com/diario-enxaqueca/documentacao/blob/main/README.md#estrutura-do-projeto)

* Testes Parametrizados
  * Backend
    * [backend/conftest.py](https://github.com/diario-enxaqueca/backend/blob/main/conftest.py)
    * [backend/source/episodio/test_episodio.py](https://github.com/diario-enxaqueca/backend/blob/main/source/episodio/test_episodio.py)
    * [backend/source/gatilho/test_gatilho.py](https://github.com/diario-enxaqueca/backend/blob/main/source/gatilho/test_gatilho.py)
    * [backend/source/medicacao/test_medicacao.py](https://github.com/diario-enxaqueca/backend/blob/main/source/medicacao/test_medicacao.py)
    * [backend/source/usuario/test_usuario.py](https://github.com/diario-enxaqueca/backend/blob/main/source/usuario/test_usuario.py)
  * Autenticação
    * [autenticacao/conftest.py](https://github.com/diario-enxaqueca/autenticacao/blob/main/conftest.py)
    * [autenticacao/auth/test_auth.py](https://github.com/diario-enxaqueca/autenticacao/blob/main/auth/test_auth.py)
  
* Testes de Integração
  * Backend
    * [backend/conftest.py](https://github.com/diario-enxaqueca/backend/blob/main/conftest.py)
    * [backend/source/episodio/test_integration_episodio.py](https://github.com/diario-enxaqueca/backend/blob/main/source/episodio/test_integration_episodio.py)
    * [backend/source/gatilho/test_integration_gatilho.py](https://github.com/diario-enxaqueca/backend/blob/main/source/gatilho/test_integration_gatilho.py)
    * [backend/source/medicacao/test_integration_medicacao.py](https://github.com/diario-enxaqueca/backend/blob/main/source/medicacao/test_integration_medicacao.py)
    * [backend/source/usuario/test_integration_usuario.py](https://github.com/diario-enxaqueca/backend/blob/main/source/usuario/test_integration_usuario.py)
  * Autenticação
    * [autenticacao/conftest.py](https://github.com/diario-enxaqueca/autenticacao/blob/main/conftest.py)
    * [autenticacao/auth/test_integration_auth.py](https://github.com/diario-enxaqueca/autenticacao/blob/main/auth/test_integration_auth.py)

* Banco de Dados
  * [backend/mysql-init/init.sql](https://github.com/diario-enxaqueca/backend/tree/main/mysql-init/init.sql)
  
* Modelo Físico do Banco
  * [Diagrama lógico](./docs/diagrama-logico.md)
  
* API em repositório separado
  * [repositório autenticacao](https://github.com/diario-enxaqueca/autenticacao/tree/main) 
  * [repositório backend](https://github.com/diario-enxaqueca/backend/tree/main)
  
* Lint ou derivados - 
  * [lint service - docker-compose.yml](./docker-compose.yml#L101)
  * [lint log](./registro-logs/lint.log)

# Ponto de Controle 3

* Front completo
  * [repositório frontend](https://github.com/diario-enxaqueca/frontend/tree/main)

* Hospedagem
  * [Diário de enxaqueca](https://frontend-production-7dfd.up.railway.app)
  
* Testes automatizados com selenium ou afins - 
  * [frontend/tests-selenium/test_diariodeenxaquecaCRUDepisodio.py](https://github.com/diario-enxaqueca/frontend/blob/main/tests-selenium/test_diariodeenxaquecaCRUDepisodio.py)
  * [frontend/tests-selenium/test_diariodeenxaquecaCRUDgatilho.py](https://github.com/diario-enxaqueca/frontend/blob/main/tests-selenium/test_diariodeenxaquecaCRUDgatilho.py)
  * [frontend/tests-selenium/test_diariodeenxaquecaCRUDmedicacao.py](https://github.com/diario-enxaqueca/frontend/blob/main/tests-selenium/test_diariodeenxaquecaCRUDmedicacao.py)
  * [frontend/tests-selenium/test_diariodeenxaquecaCRUDusuario.py](https://github.com/diario-enxaqueca/frontend/blob/main/tests-selenium/test_diariodeenxaquecaCRUDusuario.py)
  * [frontend/tests-selenium/test_diariodeenxaquecaloginlogout.py](https://github.com/diario-enxaqueca/frontend/blob/main/tests-selenium/test_diariodeenxaquecaloginlogout.py)
