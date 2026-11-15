# Manual de primeiro contato — WMK Craft Studio 0.1

## Requisitos

- Windows 10/11 x64 para o executável gerado no GitHub Actions.
- Alternativamente, Python 3.12 ou posterior com Tkinter instalado para iniciar pelo código-fonte.
- Não exige chave de IA, Node.js ou Rust para utilizar o gerenciador de projetos desta etapa.

## Abrir pelo código-fonte

Na pasta do projeto, execute:

```powershell
python main.py
```

No Windows, é possível criar um ambiente virtual, mas não é obrigatório: a interface usa somente bibliotecas da instalação padrão do Python.

## Gerar o executável pelo GitHub Actions

1. Abra a aba **Actions** do repositório WMK-Craft-Studio.
2. Selecione **WMK Craft Studio - Testes e Windows x64**.
3. Clique em **Run workflow**, selecione a branch e execute.
4. Confirme que os jobs **Testes do núcleo** e **Compilar Windows x64** foram concluídos.
5. Na execução, baixe o artefato **WMK-Craft-Studio-Windows-x64**.
6. Extraia os ZIPs até ver a pasta com `WMK-Craft-Studio.exe` e `_internal`.
7. Mantenha a pasta `_internal` ao lado do executável e abra o EXE.

**Atenção:** um ZIP portátil do PyInstaller em modo `--onedir` não consiste apenas do EXE. Ele também necessita dos arquivos em `_internal`. O software ainda não está assinado digitalmente.

## Trabalhar com projetos

Clique em **Novo projeto**, informe nome, tipo e descrição. A galeria à esquerda permite alternar entre projetos; use a pesquisa para localizar um deles. A aba **Tarefas** permite cadastrar, marcar como concluído, reabrir e excluir itens.

Use **Salvar projeto** ou Ctrl+S. O programa também salva o conteúdo do campo descrição ao trocar de projeto ou encerrar normalmente.

Use **Copiar relatório MD** ou **Salvar relatório MD** na aba Histórico. O relatório contém descrição, tarefas e eventos. Os projetos são criados em:

```text
Documentos/WMK-Craft-Studio/Projetos/<identificador>/
    wmk_project.json
    arquivos/
    logs/
    relatorios/
        estado.md  (criado ao exportar)
```

Se a pasta Documentos não existir, o programa utiliza a pasta pessoal do usuário.

O arquivo de projeto é salvo com troca atômica do arquivo temporário. Isso reduz o risco de corrupção por interrupção durante gravações, mas **não substitui backup**.

## Integrações

A aba **Ferramentas** apenas verifica se `craft-anything-cli`, `node`, `npx` e `git` estão no PATH. A presença do comando **não** comprova que ele esteja instalado corretamente, nem que o aplicativo já possa utilizá-lo.

Nenhuma ferramenta externa é executada automaticamente nesta versão. O REA não integra o WMK Craft Studio.

## Estudo funcional — alternativas originais

Na aba **Estudo funcional**, registre uma referência opcional, funcionalidades observadas legitimamente, necessidades dos usuários, a solução original que pretende produzir e diferenciais. Não envie arquivos protegidos nem reproduza interfaces, marcas ou código de terceiros.

Clique em **Copiar proposta MD** ou **Salvar proposta MD**. O relatório `alternativa-original.md` será criado na pasta `relatorios/` do projeto.

A ferramenta **não** lê executáveis, não examina código de terceiros nem gera automaticamente versões de outro programa. Esta etapa apenas organiza observações feitas pelo usuário.

Consulte a [Política de Originalidade](POLITICA_DE_ORIGINALIDADE.md). A integração opcional com o [FreeLLMAPI](PROVEDORES_IA.md) ainda é um plano, não uma funcionalidade pronta.

## Autoteste

Para validar gravação e leitura sem abrir a janela:

```powershell
python main.py --self-test .\teste-wmk
```

O comando cria um projeto de teste na pasta informada; não use uma pasta que já contenha esse projeto, pois a criação intencionalmente rejeita duplicatas.

## Limitações da versão

Ainda não existem: geração de jogos, editor de código, agentes autônomos, integração MCP efetiva, testes visuais independentes ou assinatura digital. O objetivo desta etapa é estabelecer uma base funcional e distribuível, com verificações automatizadas.

## Créditos

Walney Moreira Klein — walneyk@hotmail.com

Licença MIT. As licenças, avisos e marcas de ferramentas externas não são incluídos neste repositório.
