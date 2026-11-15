# Roadmap — WMK Craft Studio

Este documento separa o que existe do que ainda precisa ser implementado. Não se deve declarar uma etapa concluída apenas porque foi planejada.

## Primeiro MVP web no-code — implementação experimental

- [x] Interface web local em português, com galeria e três painéis ajustáveis
- [x] Criar um site original de demonstração a partir de título, descrição, tipo e cor
- [x] Exibir a aplicação gerada em iframe sandboxed, com opção de celular/desktop
- [x] Alterações guiadas por comandos simples em português (não IA)
- [x] Visualizar HTML/CSS/JS e baixar ZIP
- [x] Testes automatizados de geração, persistência, API e origem das requisições
- [x] Empacotamento Windows (workflow configurado; confirmar sucesso do build)
- [ ] Gerar sites com modelo de IA, mudanças livres e assets próprios/licenciados
- [ ] Editor de código com salvamento, versão anterior e testes de regressão
- [ ] Aplicativo administrativo com banco SQLite e jogo 2D jogável

Veja [PRIMEIRO-SITE.md](PRIMEIRO-SITE.md). Este marco não substitui a exigência de geração full-stack.

## Direção prioritária — experiência sem código

**Público:** iniciantes que desejam criar sites, web apps e jogos 2D sem dominar programação.

- [ ] Substituir a interface do protótipo inicial por um Studio web local com **prompt + prévia executável + chat de mudanças**.
- [ ] Galeria com **Site**, **Aplicativo** e **Jogo 2D**, cada categoria começando com **um template autoral verificado**.
- [ ] Adaptar um motor de geração web, após POC, sem copiar programas de terceiros.
- [ ] Oferecer botão **Criar**, **Testar**, **Corrigir**, **Baixar projeto** e **Publicar**, com interface inteiramente em português.
- [ ] Preservar uma área **Avançado** para código, erros, logs, parâmetros, consumo de IA e relatórios.
- [ ] Garantir que uma aplicação gerada seja realmente executável e passe por testes independentes.
- [ ] Manter FreeLLMAPI opcional e funcionamento offline limitado a templates e edição manual.

Detalhes: [EXPERIENCIA-SEM-CODIGO.md](EXPERIENCIA-SEM-CODIGO.md), [VISAO-APP-BUILDER.md](VISAO-APP-BUILDER.md) e [INVENTARIO-DE-FORKS.md](INVENTARIO-DE-FORKS.md).

**Nota:** os itens abaixo descrevem fases da fundação desktop antiga. A fundação não implementa ainda geração ou prévia por conversa.

## Etapa 0.1 — Fundação desktop (implementada nesta branch)

- [x] Aplicativo desktop em português (Tkinter / Python padrão)
- [x] Interface escura com divisor de painéis ajustável
- [x] Galeria de projetos locais
- [x] Criar, reabrir e salvar projetos em JSON com gravação atômica
- [x] Tipos: livre, web, desktop e jogo (classificação, **não** geração)
- [x] Estudo funcional: observações permitidas, necessidades e proposta autoral em Markdown
- [x] Registro de tarefas e histórico
- [x] Copiar e salvar relatório Markdown
- [x] Detectar ferramentas externas presentes no PATH, **sem executá-las**
- [x] Workflow para testes e empacotamento Windows x64
- [x] Autoteste de EXE que escreve e relê um projeto sem abrir janela
- [x] Compilação e testes Linux/Windows aprovados em [execução #43673881491](https://github.com/WalneyNF/WMK-Craft-Studio/actions/runs/43673881491); compila EXE, executa autoteste e envia ZIP portátil
- [ ] Testar visualmente o executável em um desktop Windows real

## Etapa 0.2 — Usabilidade e projetos

- [ ] Templates verificáveis: tarefas/web local e cadastro SQLite
- [ ] Importação e backup de projetos
- [ ] Versões e restauração de arquivos
- [ ] Painéis destacáveis e layouts nomeados; nesta fase há somente divisor ajustável
- [ ] Editor de arquivos com confirmação para salvar
- [ ] Exportar logs de execução e dossiê integral por etapa

## Etapa 0.3 — Motor Craft Anything

- [ ] Adaptador para processos externos sem shell, com permissões explícitas
- [ ] Detectar versão real da CLI antes de oferecer ações
- [ ] Importar resultados para pasta de projeto
- [ ] Coletar saída e erros com carimbo de data
- [ ] Restrições por diretório de trabalho, limites de tempo e cancelamento
- [ ] Testes de integração com comandos reais e resultados verificáveis

## Etapa 0.4 — Provedores de IA: FreeLLMAPI e alternativas

- [ ] Detectar serviço local FreeLLMAPI somente em loopback, sem expor chaves
- [ ] Configurar acesso à API compatível com OpenAI por perfil e projeto
- [ ] Segregar dados e confirmar consentimento antes de enviá-los a modelos remotos
- [ ] Exibir modelos disponíveis, perfis, custos e limites de uso
- [ ] Permitir funcionamento sem API/IA, mantendo templates e armazenamento locais
- [ ] Criar assistentes para **abstrair requisitos e implementar soluções originais**
- [ ] Rejeitar solicitações de clonagem, extração de código ou engenharia reversa

Veja [PROVEDORES_IA.md](PROVEDORES_IA.md). O FreeLLMAPI é opcional; o REA não integra este produto.

## Etapa 0.5 — Quality Gate independente

- [ ] Testes de comportamento executados por observador independente do aplicativo gerado
- [ ] Screenshot real com comparação e critérios mensuráveis
- [ ] Verificações de armazenamento, API e interface
- [ ] Relatórios que incluam sucesso, falha, evidência e comando de reprodução
- [ ] Compilação e empacotamento vinculados ao hash da revisão

## Etapa 1.0 — Produto distribuível

- [ ] Instalação/atualização e documentação de primeiro contato
- [ ] Assinatura de executáveis quando houver certificado
- [ ] Empacotamento multiplataforma verificado
- [ ] Templates de jogos e aplicativos submetidos a testes reais
- [ ] Traduções e acessibilidade revisadas

## Princípios

1. O fluxo de trabalho nunca pode reduzir requisitos aprovados silenciosamente.
2. Resultados gerados por IA são propostas até terem evidências independentes.
3. A aplicação local deve continuar útil sem chave de IA.
4. Segredos ficam fora do repositório e não aparecem em logs.
5. As integrações permanecem separadas para permitir atualização dos forks.
6. O produto nunca poderá se tornar ferramenta de clonagem ou engenharia reversa: veja [POLITICA_DE_ORIGINALIDADE.md](POLITICA_DE_ORIGINALIDADE.md).
