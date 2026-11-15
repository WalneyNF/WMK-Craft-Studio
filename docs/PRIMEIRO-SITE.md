# WMK Craft Studio Web — crie seu primeiro site sem programar

**Situação:** primeiro MVP de criação **local por templates, sem inteligência artificial**. O sistema não gera qualquer projeto a partir de linguagem natural irrestrita; oferece um fluxo funcional e seguro para criação, personalização e exportação de **sites demonstrativos**.

## No Windows 10/11

1. Baixe a branch **feat/studio-web-no-code-mvp** como ZIP no GitHub e extraia todos os arquivos.
2. Com Python 3.12 ou mais recente, dê duplo clique em `INICIAR-STUDIO-WEB.cmd`.
3. O navegador abre em `http://127.0.0.1:8765`. Se não abrir automaticamente, digite esse endereço no navegador.
4. Digite o nome da sua empresa ou projeto, descreva o que deseja apresentar, selecione modelo e cor.
5. Clique em **Criar site e visualizar**. A prévia mostra o HTML/CSS realmente salvo no disco.
6. Experimente **Mude a cor para azul**, **Altere o título para Meu Site** ou **Adicione uma seção sobre Serviços**.
7. Clique em **Baixar ZIP**, extraia e abra `index.html` sem precisar do WMK.

Para encerrar o servidor, volte ao terminal aberto e pressione **Ctrl+C**.

### Execução manual

```powershell
python studio_web.py --open
```

Para usar outra porta ou pasta de projetos:

```powershell
python studio_web.py --port 8767 --root "D:\Ferramentas\WMK-Meus-Projetos" --open
```

Esse aplicativo funciona sem bibliotecas externas, GPU, chave de IA ou Node.js. Os sites exportados têm HTML, CSS e JS estáticos.

## Comandos de alteração disponíveis

- **Mude a cor para azul** (verde, azul, roxo, laranja, rosa, vermelho, preto, dourado)
- **Altere o título para Novo Nome**
- **Mude o texto principal para Uma nova descrição**
- **Adicione uma seção sobre Nossa equipe** (até 5 seções extras)

**Limitação:** estes comandos são reconhecidos por regras fixas; **não** são atendidos por um modelo de IA. Pedidos desconhecidos geram aviso e não são declarados como executados.

## O que foi implementado

- Galeria local com busca.
- Criar três tipos de sites: institucional, vitrine e portfólio.
- Renderizar uma prévia real em iframe isolado.
- Inspecionar HTML, CSS e JS em modo leitura.
- Pedir mudanças simples por texto.
- Testar visualização na largura de celular ou desktop.
- Baixar pacote ZIP completo com instruções.
- Layout com largura ajustável e preferências locais no navegador.
- API e servidor HTTP de uso local com autenticação de origem de requisições mutáveis.
- Testes automatizados de criação, persistência, HTML escapado, exportação e API.

## O que ainda NÃO faz

- Não conversa com FreeLLMAPI nem outros modelos de IA.
- Não cria aplicações com banco de dados, sistemas financeiros ou jogos automaticamente.
- Vitrine é **demonstrativa**, sem checkout, carrinho, pedidos ou integração de pagamento.
- Não possui hospedagem nem publicação automática.
- Não incorpora recursos visuais de terceiros ou reproduz sites comerciais.
- Não salva mudanças de código diretamente na aba Código.
- Não constitui ambiente isolado para executar código arbitrário de terceiros. Somente os templates autorais são gerados.

## Segurança

O servidor escuta **somente 127.0.0.1**. Não o exponha pela rede ou internet. A prévia utiliza iframe sandbox sem `allow-same-origin`; o site exportado é estático. Ao publicar, substitua textos ilustrativos por conteúdo real e revise direitos de imagens, legislação aplicável e acessibilidade.

Os projetos são guardados na pasta de projetos padrão do WMK (Documentos/WMK-Craft-Studio/Projetos) ou na pasta indicada por `--root`.

## Como testar

```powershell
python -m unittest discover -s tests -v
python -m py_compile studio_web.py site_factory.py
```

Documentos complementares: [Experiência sem código](EXPERIENCIA-SEM-CODIGO.md) e [Política de originalidade](POLITICA_DE_ORIGINALIDADE.md).

**Walney Moreira Klein — walneyk@hotmail.com**
