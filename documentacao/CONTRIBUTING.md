# Contributing to Diário de Enxaqueca – Documentação

Obrigado por contribuir com a documentação do Diário de Enxaqueca! Este repositório organiza MVP, backlog, regras de negócio, diagramas UML e protótipo Figma. Seguir estas diretrizes garante consistência e rastreabilidade no projeto.

## Como contribuir
#### Clonar o repositório

Clone o repositório localmente:
```bash
git clone https://github.com/diario-enxaqueca/documentacao.git
cd documentacao
```
####  Criar branch

Crie uma nova branch a partir da branch principal (`main`):
```bash
git checkout main
git pull
git checkout -b feature/nova-documentacao
```

Use nomes descritivos, como `feature/uml-episodio` ou `docs/backlog-mvp`.

####  Fazer commits

Siga o padrão Conventional Commits:
```php-template
<tipo>[escopo opcional]: <descrição>
```

Tipos comuns:

* `docs` – Atualização ou adição de documentação
* `feat` – Nova seção ou funcionalidade documentada
* `fix` – Correção de erros na documentação
* `style` – Ajustes de formatação

Exemplo:
```bash
git commit -m "docs(uml): adiciona diagrama de classes do CRUD de episodios"
```
####  Abrir Pull Request

1. Faça push da branch:
```bash
git push origin feature/nova-documentacao
```
2. Abra um Pull Request para a branch `main`.
3. Forneça descrição detalhada do que foi adicionado ou modificado.
4. Aguarde revisão e comentários antes de merge.

## Boas práticas

* Organize arquivos em pastas correspondentes (`historias_usuario/`, `uml/`, `prototipo_figma/`, `regras_negocio/`).
* Inclua **links**, **PDFs**, **capturas de tela** quando necessário.
* Siga o **padrão de nomenclatura** consistente para arquivos e pastas.
* Atualize **MVP**, **backlog** e **regras de negócio** sempre que houver mudanças no projeto.
* Documente cada diagrama **UML** e protótipo Figma com explicação clara.

## Agradecimento

Obrigado por manter a documentação organizada e completa! Cada contribuição garante que todos os membros do projeto possam entender, desenvolver e manter o Diário de Enxaqueca de forma eficiente.