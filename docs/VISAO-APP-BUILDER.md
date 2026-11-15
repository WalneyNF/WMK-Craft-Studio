# WMK Craft Studio — visão de produto: criação de aplicativos por conversa

**Data de referência:** 15/11/2026  
**Status:** especificação de produto, **não** funcionalidade pronta.  
**Referência de fluxo:** [Google AI Studio — Build Apps](https://ai.google.dev/gemini-api/docs/aistudio-build-mode?hl=pt-BR). O WMK deve adotar o conceito de prompt → geração → prévia → edição → testes → publicação, **sem copiar interface, código, ativos ou marcas**.

## Visão

Um usuário descreve um software original em português, escolhe plataforma e requisitos, acompanha a geração de arquivos e visualiza o aplicativo **executando de verdade**. Ele pode modificar o projeto por chat ou por seleção visual de componentes, editar código, comparar versões e exportar a entrega com testes reproduzíveis.

**Tipos-alvo:** sites, web apps full-stack, ferramentas de gestão/finanças, lojas virtuais, jogos 2D em navegador e, em fases posteriores, Android e desktop. **Nenhum modelo de IA promete software perfeito nem elimina homologação humana.**

## Experiência prioritária

### Galeria de aplicativos

- Novo projeto com prompt; opções web, app administrativo e jogo 2D.
- Templates **próprios**, verificados por testes, com imagens reais do projeto gerado.
- Projetos existentes com pesquisa, miniaturas, última execução, estado e versões.
- Importar código de repositórios próprios ou com autorização; sem clonagem de produtos.

### Studio de três áreas

- **Esquerda:** projetos, arquivos, assets e versões.
- **Centro:** conversa com IA, contrato de requisitos, tarefas, logs e custos/tokens.
- **Direita:** abas Prévia, Código, Testes, Banco de Dados e Entrega.
- Painéis redimensionáveis e destacáveis, layouts nomeados e persistidos em JSON.
- Desenhar/selecionar elemento da prévia para solicitar mudança: o agente recebe ID do componente próprio, limites e instrução; nunca copia interface de terceiros.
- Botões Copiar, Copiar MD e Salvar MD em contratos, logs, agentes e relatórios.

### Pipeline verificável

```text
Prompt em português
   ↓
Classificador (tipo de projeto e stack) → template testado
   ↓
Contrato versionado (requisitos e critérios não reduzíveis)
   ↓
Construtor com permissões e pasta isolada
   ↓
Instalação de dependências e execução instrumentada
   ↓
Prévia em sandbox + editor de arquivos
   ↓
Testador independente (funcional, dados, segurança, UI)
   ├─ falha → correção limitada → repetição dos testes
   └─ passa → ZIP, código, relatório, GitHub Actions e publicação opcional
```

**Não basta compilar.** Testes precisam comprovar operações reais; o agente não pode aprovar a própria entrega sem verificador independente.

## Arquitetura escolhida para MVP

### Casca e núcleo

- Manter a versão desktop Tkinter v0.1 **somente como protótipo de gerenciamento**, sem tratá-la como interface definitiva de geração de apps.
- Evoluir para **Studio web local-first** com React + TypeScript e backend Node.js 22+ (ou processo servidor equivalente tecnicamente verificado), iniciado por launcher Windows.
- Projetos em pastas, manifestos JSON versionados, banco SQLite local para índices/execuções e armazenamento de backups.
- Editor Monaco; prévia de aplicativos web em iframe com origem separada e restrições de CSP; servidor de desenvolvimento de cada projeto em processo/container isolado.
- Executor sem `shell=true` por padrão; permissões para arquivos/comandos/rede, limites de CPU/memória/tempo, cancelamento e logs.
- O projeto gerado **não** tem acesso às credenciais, arquivos do WMK ou chaves de provedores. Prévia isolada não deve compartilhar cookies ou origem com painel e API do Studio.
- Testes automatizados no host CI e testes reais de navegador (Playwright), inclusive persistência e respostas HTTP.

### Agentes e modelos

- **FreeLLMAPI**: candidato prioritário de gateway de modelos via API compatível com OpenAI. Opcional; usuários podem configurar outro endpoint compatível. Chaves em armazenamento seguro, não nos projetos.
- **bolt.diy**: candidato prioritário a *referência de engine de construção web*; testar contrato e licença antes de reutilizar componentes. Seu código atual depende de Remix/Cloudflare e WebContainers, portanto **não é um motor plug-and-play** do WMK.
- **Craft Anything**: candidato a executor externo de projetos **originais** em operações permitidas; **desabilitar integralmente** inspeção/comparação/replicação de software de terceiros.
- **Hallmark ou Taste Skill**: direção visual, escolhida por projeto, nunca duas regras conflitantes ao mesmo tempo.
- **Impeccable**: detector de qualidade visual com saída estruturada (após isolamento de processos). **Não usar Live mode que desabilita aprovações e sandbox de agentes.**
- **Blockly**: biblioteca para modo visual de regras, após a versão básica da IDE estar funcional.

### Motores por tipo de projeto

| Perfil | Primeira stack | Critérios mínimos |
| --- | --- | --- |
| Site HTML | HTML/CSS/JS + Vite opcional | Link, formulário, navegação, responsividade, acessibilidade, screenshot |
| Aplicativo administrativo | React + API Node + SQLite | CRUD, filtros, dados persistentes, migrações, autenticação, backup |
| Controle financeiro | Web stack + armazenamento transacional | Montantes decimais, saldos reconciliados, auditoria, segregação por usuário |
| Loja virtual | Web full-stack, checkout simulado | Carrinho, estoque, pedido, webhook de sandbox, segurança e LGPD |
| Plataforma 2D original | Phaser para navegador (template autoral) | Controles, salto, colisões, câmera, morte, checkpoint, final de fase |
| Jogo 2D desktop | Godot/GDevelop em etapa posterior | Projeto editável, assets licenciados, input real, export, testes de cena |

Nada de prometer pagamentos reais ou produção financeira sem avaliação específica de segurança.

## Contrato de projeto (conceitual)

```json
{
  "schema_version": 1,
  "kind": "webapp",
  "name": "Controle Financeiro WMK",
  "brief": "Gerenciar receitas e despesas...",
  "stack": {"frontend": "react", "backend": "node", "database": "sqlite"},
  "requirements": [
    {"id": "RF-001", "text": "Registrar despesa", "required": true,
     "acceptance_tests": ["Criar despesa e confirmar no banco após reiniciar"]}
  ],
  "project_root": "arquivos/",
  "steps": [],
  "runs": [],
  "evidence": []
}
```

O campo `requirements` é append-only entre revisões aprovadas: mudanças só por decisão explícita do usuário. Retornos de LLM não constituem evidência.

## Etapas de entrega

### M1 — Studio web funcional

- [ ] Galeria real de projetos, prompt e arquivos persistidos.
- [ ] Layout ajustável com três áreas e temas em pt-BR.
- [ ] Criar projeto a partir de **um template autoral testado**, gerar arquivo e abrir prévia em execução real.
- [ ] Editar arquivo no Monaco, salvar e atualizar prévia; histórico e rollback.
- [ ] Testes do núcleo e distribuição Windows com launcher local.

### M2 — Construção por IA

- [ ] Gateway FreeLLMAPI opcional com teste de conexão e modelo selecionável.
- [ ] Agente produz alterações multi-arquivo em diff validado, com política de permissões.
- [ ] Compilação e execução instrumentadas; logs, erros e cancelamento.
- [ ] Alterações incrementais com conversa e confirmação de mudanças perigosas.
- [ ] Critérios de aceitação preservados e exportáveis Markdown.

### M3 — Qualidade e publicação

- [ ] Auditorias Impeccable (somente execução segura de CLI).
- [ ] Testes Playwright em telas responsivas, fluxos CRUD e regressão visual.
- [ ] ZIP com código e README, GitHub Actions e preview publicável mediante confirmação.
- [ ] Registro de dependências, licenças, proveniência de assets e ameaças.

### M4 — Fábrica de jogos

- [ ] Template Phaser original de plataforma 2D com sprites licenciados.
- [ ] Preview de jogo executável, testes de input/colisão/progressão.
- [ ] Editor visual de lógica com Blockly e cenas/objetos.
- [ ] Integração opcional com WMK Game Studio/GDevelop ou Godot após POC.

### M5 — Edição visual avançada e plataformas adicionais

- [ ] Seleção/inspeção de elementos na prévia e edição por conversa.
- [ ] Integração visual com GrapesJS ou WMK App Builder, conforme POC.
- [ ] Android nativo, aplicativos desktop e multiusuário somente após validação de segurança/empacotamento.

## Três projetos de aceitação obrigatórios

1. **Controle financeiro:** banco de dados real, valores decimais, CRUD, relatórios, reinício com dados preservados e testes de segurança.
2. **Loja virtual:** catálogo, carrinho, pedidos, estoque e pagamento **somente em sandbox**, com verificação de concorrência e erros.
3. **Plataforma 2D original:** input, movimentação, gravidade, colisão, inimigo, checkpoints, pontuação e conclusão de fase (sem personagens, mapas ou músicas de terceiros).

Cada projeto precisa ser reaberto, alterado e reconstruído. Uma captura de tela não comprova funcionamento.

## Leis, licenças e originalidade

- [Política de originalidade](POLITICA_DE_ORIGINALIDADE.md) obrigatória. Não clonar produtos, fazer engenharia reversa, descompilar ou copiar código e assets protegidos.
- Preservar copyright e licenças de cada fork; não incorporar aplicações inteiras sem necessidade.
- Repositórios source-available ou com componentes enterprise não são automaticamente incorporáveis em app MIT.
- Dados do cliente podem ser enviados a modelos externos: exigir consentimento e mostrar destino e custo previsto.
- Referência Google AI Studio: reproduzir **apenas padrão geral de utilização**, sem marcas, elementos gráficos proprietários ou código do Google.

## Evidências consultadas

- Google AI Studio oficial: https://ai.google.dev/gemini-api/docs/aistudio-build-mode?hl=pt-BR
- Comparação e inventário dos forks: [INVENTARIO-DE-FORKS.md](INVENTARIO-DE-FORKS.md)
- Provedores: [PROVEDORES_IA.md](PROVEDORES_IA.md)
- Roadmap base: [ROADMAP.md](ROADMAP.md)

**Walney Moreira Klein — walneyk@hotmail.com**
