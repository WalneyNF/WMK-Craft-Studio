# Experiência sem código — WMK Craft Studio

**Público principal:** pessoas sem experiência em programação.  
**Meta do produto:** permitir que alguém crie **um site, um web app ou um jogo 2D original**, veja o resultado funcionando e melhore por conversa, sem escrever código.  
**Status:** especificação aprovada pelo direcionamento do projeto; funcionalidades futuras, não confundir com o aplicativo Tkinter v0.1.

## Promessa central

> Conte sua ideia em português. Escolha uma aparência ou comece com modelo pronto. Veja sua criação funcionar. Peça mudanças por conversa. Publique quando os testes essenciais estiverem aprovados.

O WMK deve explicar o que está fazendo em palavras simples, com opção **Avançado** para os interessados em programação. Não obrigar instalação manual de terminal, SDK ou banco de dados para começar.

### Três portas de entrada

**Criar site** — institucional, portfólio, eventos, cardápio, vitrine ou loja virtual inicial.

**Criar aplicativo** — finanças pessoais, agenda, orçamentos, estoque, clientes e pequenas operações comerciais.

**Criar jogo 2D** — plataforma, quebra-cabeça, aventura original, jogo educativo ou clicker.

Cada opção começa por um **template de qualidade já testado**, não por uma IA inventando arquitetura e imagens do zero. Templates são extensíveis e nunca devem gerar cópias de jogos/marcas de terceiros.

## Fluxo de primeiro contato (iniciante)

1. **O que deseja criar?** Três cartões grandes: Site, Aplicativo ou Jogo.
2. **Descreva com suas palavras.** Um campo simples e sugestões de exemplos editáveis.
3. **Confirme o resumo.** O WMK exibe uma ficha legível: objetivos, telas, funcionalidades, dados e critérios mínimos de funcionamento. Perguntar apenas o essencial.
4. **Criar primeira versão.** Usar template original confiável; agente adiciona recursos de forma incremental.
5. **Ver funcionando.** Prévia real à direita. O usuário pode navegar, preencher formulários ou jogar.
6. **Peça uma alteração.** Ex.: "Mude a cor", "Acrescente um cadastro", "O personagem precisa de pulo duplo".
7. **Teste em linguagem comum.** Ex.: "Consegui cadastrar produto", "Dados continuaram após fechar", "Cheguei ao fim da fase".
8. **Entregar.** Botões: **Baixar projeto**, **Baixar site/jogo**, **Publicar** (quando apropriado), **Como usar**.

Não expor opções como CLI, React, Vite, migrations, auth scopes ou CI/CD no modo iniciante. Mostrá-las apenas sob **Detalhes técnicos**.

## Telas do produto

- **Início:** "O que você quer criar hoje?" + galeria de criações do usuário + biblioteca de exemplos autorais.
- **Studio:** conversa + prévia real em destaque; arquivos, tarefas e logs em painéis opcionais. Painéis móveis/redimensionáveis com layouts salvos por usuário.
- **Meus projetos:** miniaturas, estado, último uso, duplicar projeto próprio, renomear, exportar, reabrir.
- **Testes:** estados **Funcionando**, **Precisa corrigir**, **Não verificado**, com evidência, não apenas autodeclaração de IA.
- **Publicar:** destino, informações pessoais e chaves de produção, exigindo confirmação explícita.

## Padrões de comunicação

| Linguagem técnica a evitar no modo simples | Como explicar |
| --- | --- |
| Instalar dependências | Preparar o projeto |
| Rodar build | Gerar versão para usar |
| Executar Playwright | Testar no navegador |
| API / endpoint | Conexão com outro serviço |
| Migration | Atualizar a estrutura dos dados |
| CLI / terminal | Ferramentas avançadas |
| Testes E2E falharam | Ao usar o sistema, encontramos um problema |
| Runtime exception | O programa apresentou um erro |

A opção **Ver detalhes** permite expandir códigos, comandos, logs, erros e JSON, inclusive copiar ou exportar MD.

## Acessibilidade e necessidades

- Interface e guias **em português brasileiro**, inclusive erros e assistente de primeiro contato.
- Fonte legível, zoom, navegação por teclado, contraste e redução de animações.
- Iniciar com poucos controles; não colocar dez painéis grandes e fixos.
- Auto-salvar e permitir voltar à versão anterior; erros não podem destruir o projeto anterior.
- Explicar quando modelos podem cobrar ou enviar dados a provedores externos.
- Informar se está **sem internet**, sem chave de IA ou sem recursos para gerar.
- IA **opcional** para uso de templates já existentes, edição manual e testes de modelos.
- Segurança: execução de código gerado isolada do computador e dos dados do usuário.

## Critérios de aceitação para três exemplos

### Site de negócio

- [ ] Iniciante informa nome/serviços e cria primeira versão sem terminal.
- [ ] Prévia abre e pode ser navegada realmente.
- [ ] Alterar texto por conversa atualiza a prévia e mantém o restante.
- [ ] Links, navegação, imagens autorizadas e visualização móvel funcionam.
- [ ] Exporta HTML/CSS/JS que abrem fora do WMK, com manual simples.

### Aplicativo de finanças pessoais

- [ ] Iniciante cria projeto sem conhecer banco de dados.
- [ ] Registra receitas/despesas e consulta saldo correto, inclusive centavos.
- [ ] Fecha e reabre a prévia sem perder dados.
- [ ] Edita uma regra por conversa sem descartar cadastros.
- [ ] Exporta backup, projeto e manual em linguagem simples.
- [ ] Verificações de autenticação e isolamento quando múltiplos usuários forem permitidos.

### Jogo de plataforma original

- [ ] Iniciante escolhe tema/estilo e vê uma fase curta jogável.
- [ ] Personagem original tem movimento, pulo, colisões, câmera e objetivo.
- [ ] Pode trocar personagem, ajustar velocidade e pulo sem editar código.
- [ ] É possível falhar, reiniciar e completar a fase, com testes correspondentes.
- [ ] Exporta jogo para navegador e projeto editável; atribuição dos assets é conhecida.
- [ ] Não copia personagens, músicas, cenários ou nomes de jogos conhecidos.

## Regra de qualidade

O usuário não deve receber como **Concluído** um projeto apenas porque a IA disse que terminou. Um verificador independente deve executar cenários reais, guardar evidências e dizer precisamente o que foi ou não comprovado.

Para aumentar a confiabilidade, cada modalidade deve começar por **um único template autoral completo** com testes regressivos; só então ampliar catálogo, temas e recursos.

## Implementação em módulos

- **No-code shell:** React + TypeScript, galeria, prompt, prévia, Monaco em painel avançado.
- **Gateway IA:** FreeLLMAPI (opcional) ou compatível OpenAI, com chaves protegidas e limites.
- **Criação de web apps:** avaliar adaptação de bolt.diy e modelos internos testados.
- **Design:** Hallmark ou Taste Skill na geração; Impeccable na verificação web.
- **Lógica visual:** Blockly, com interface de eventos e saída de código autoral.
- **Jogos 2D:** começar com template Phaser independente; usar WMK Game Studio/GDevelop ou ct.js como ferramentas externas conforme prova de conceito.
- **QA:** testes automatizados no navegador e evidências de dados e interações.
- **Build:** GitHub Actions e exportações; sem publicação automática sem consentimento.

## Direitos e segurança

É um sistema para **criações independentes e autorais**, não um clonador. Não deve fazer engenharia reversa, descompilar ou reproduzir conteúdo de terceiros. Ler e aplicar [POLITICA_DE_ORIGINALIDADE.md](POLITICA_DE_ORIGINALIDADE.md).

**Walney Moreira Klein — walneyk@hotmail.com**
