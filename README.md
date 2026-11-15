# WMK Craft Studio

**Fábrica de software com foco em projetos verificáveis, interfaces acessíveis e código-fonte aberto.**

> Status: projeto em desenvolvimento. A versão inicial prioriza um gerenciador de projetos local para Windows, antes de integrar agentes de IA ou engenharia reversa.

## Objetivo

Permitir criar e administrar projetos de software com transparência: planejamento, arquivos, histórico de execução, relatórios e, futuramente, geração assistida por IA e testes independentes.

## Componentes

- **WMK Craft Studio (este repositório):** aplicativo, projetos locais, interface e orquestração.
- [Craft Anything](https://github.com/WalneyNF/craft-anything): motor externo de geração/inspeção a integrar por adaptador.
- [REA](https://github.com/WalneyNF/rea): ferramenta externa de engenharia reversa a integrar via MCP.

Os motores permanecem em repositórios separados. Nenhuma integração é anunciada como funcional sem teste correspondente.

## Próximos passos

1. Interface desktop em português e projetos persistidos em JSON.
2. Testes e compilação Windows via GitHub Actions.
3. Templates úteis, editor de projetos e relatórios Markdown.
4. Adaptação de agentes e do REA via processos isolados/MCP.
5. Verificações independentes de comportamento e qualidade visual.

## Créditos

**Walney Moreira Klein — walneyk@hotmail.com**

A utilização de componentes externos respeitará suas licenças e avisos de atribuição.
